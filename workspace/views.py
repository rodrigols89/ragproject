import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FolderForm
from .models import File, Folder
from .validators import validate_file


@login_required(login_url="/")
def workspace_home(request):
    folder_id = request.GET.get("folder")

    # 📁 1. Se o usuário clicou em alguma pasta
    if folder_id:
        current_folder = get_object_or_404(
            Folder, id=folder_id, owner=request.user
        )

        # Subpastas da pasta atual
        folders = Folder.objects.filter(
            parent=current_folder, is_deleted=False
        )

        # Arquivos da pasta atual
        files = File.objects.filter(
            folder=current_folder, is_deleted=False
        )

        # Breadcrumbs (caminho completo)
        breadcrumbs = []
        temp = current_folder
        while temp:
            breadcrumbs.append(temp)
            temp = temp.parent
        breadcrumbs.reverse()

    else:
        # 📁 2. Estamos no nível raiz
        current_folder = None

        folders = Folder.objects.filter(
            owner=request.user, parent__isnull=True, is_deleted=False
        )

        files = File.objects.filter(
            uploader=request.user, folder__isnull=True, is_deleted=False
        )

        breadcrumbs = []  # Raiz não tem caminho

    context = {
        "current_folder": current_folder,
        "folders": folders,
        "files": files,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "pages/workspace_home.html", context)


@login_required(login_url="/")
def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)

        # Obter a pasta pai (se aplicável)
        parent_id = request.POST.get("parent")
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(
                Folder, id=parent_id, owner=request.user
            )

        if form.is_valid():
            name = form.cleaned_data["name"]

            # Verificar duplicação (ignorando caixa alta/baixa)
            if Folder.objects.filter(
                owner=request.user, name__iexact=name, parent=parent_folder
            ).exists():
                form.add_error(
                    "name",
                    "Já existe uma pasta com esse nome nesse diretório.",
                )
            else:
                # Criar nova pasta
                new_folder = form.save(commit=False)
                new_folder.owner = request.user
                new_folder.parent = parent_folder
                new_folder.save()

                messages.success(
                    request, f"Pasta '{name}' criada com sucesso!"
                )
                return redirect(request.POST.get("next", "workspace_home"))

        # ---------------------------------------------------------------
        # ❗ Se houver erro, reconstruir contexto da pasta correta
        # ---------------------------------------------------------------

        # Recupere novamente *tudo* como na workspace_home
        if parent_folder:
            # Estamos dentro de uma pasta
            folders = Folder.objects.filter(
                parent=parent_folder, is_deleted=False
            )
            files = File.objects.filter(
                folder=parent_folder, is_deleted=False
            )
            breadcrumbs = build_breadcrumbs(parent_folder)
        else:
            # Estamos na raiz
            folders = Folder.objects.filter(
                owner=request.user, parent__isnull=True, is_deleted=False
            )
            files = File.objects.filter(
                uploader=request.user, folder__isnull=True, is_deleted=False
            )
            breadcrumbs = []

        context = {
            "form": form,
            "current_folder": parent_folder,
            "folders": folders,
            "files": files,
            "breadcrumbs": breadcrumbs,
            "show_modal": True,  # reabrir modal com erro
        }
        return render(request, "pages/workspace_home.html", context)

    # Se método não for POST, redireciona para a home
    return redirect("workspace_home")


@login_required(login_url="/")
def upload_file(request):
    """
    View que faz upload de arquivos com:
    - validação de extensão
    - validação de tamanho
    - renome automático em caso de duplicação
    """
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        next_url = request.POST.get("next", "workspace_home")
        folder_id = request.POST.get("folder")
        folder = None

        # pegar pasta atual se existir
        if folder_id:
            folder = get_object_or_404(
                Folder, id=folder_id, owner=request.user
            )

        # nenhum arquivo enviado
        if not uploaded_file:
            messages.error(request, "Nenhum arquivo foi enviado.")
            return redirect(next_url)

        # ------------------------------
        # 🔍 Validações via validators.py
        # ------------------------------
        try:
            validate_file(uploaded_file)
        except Exception as e:
            # pega somente a mensagem, não a lista
            messages.error(request, e.message)
            return redirect(next_url)

        # -------------------------------------
        # 🔄 Renome automático em caso de duplicação
        # -------------------------------------
        original_name = uploaded_file.name
        base, ext = os.path.splitext(original_name)
        new_name = original_name
        counter = 1

        while File.objects.filter(
            uploader=request.user, folder=folder, name__iexact=new_name
        ).exists():
            new_name = f"{base} ({counter}){ext}"
            counter += 1

        # ------------------------------
        # 💾 Criação do arquivo
        # ------------------------------
        File.objects.create(
            name=new_name,
            file=uploaded_file,
            folder=folder,
            uploader=request.user,
        )

        messages.success(request, f"Arquivo '{new_name}' enviado com sucesso!")
        return redirect(next_url)

    return redirect("workspace_home")


def build_breadcrumbs(folder):
    """
    Constrói a lista de breadcrumbs (caminho completo)
    desde a raiz até a pasta atual.
    """
    breadcrumbs = []
    while folder:
        breadcrumbs.insert(0, folder)
        folder = folder.parent
    return breadcrumbs


@login_required(login_url="/")
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    # pasta pai p/ retornar após exclusão
    parent = folder.parent

    folder.is_deleted = True
    folder.deleted_at = timezone.now()
    folder.save()

    messages.success(request, f"Pasta '{folder.name}' movida para a lixeira.")

    if parent:
        return redirect(f"/workspace?folder={parent.id}")

    return redirect("workspace_home")


@login_required(login_url="/")
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, uploader=request.user)

    folder = file.folder

    file.is_deleted = True
    file.deleted_at = timezone.now()
    file.save()

    messages.success(request, f"Arquivo '{file.name}' movido para a lixeira.")

    if folder:
        return redirect(f"/workspace?folder={folder.id}")

    return redirect("workspace_home")


@login_required(login_url="/")
def rename_folder(request, folder_id):
    folder = get_object_or_404(
        Folder, id=folder_id, owner=request.user, is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    if not new_name:
        messages.error(request, "O nome da pasta não pode ser vazio.")
        return redirect(next_url)

    # impedir duplicatas no mesmo parent (case-insensitive), exceto a própria
    if Folder.objects.filter(
        owner=request.user,
        parent=folder.parent,
        name__iexact=new_name,
    ).exclude(id=folder.id).exists():
        messages.error(
            request, "Já existe uma pasta com esse nome nesse diretório."
        )
        return redirect(next_url)

    folder.name = new_name
    folder.save()
    messages.success(request, f"Pasta renomeada para '{new_name}'.")
    return redirect(next_url)


@login_required(login_url="/")
def rename_file(request, file_id):
    file = get_object_or_404(
        File, id=file_id, uploader=request.user, is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    if not new_name:
        messages.error(request, "O nome do arquivo não pode ser vazio.")
        return redirect(next_url)

    # impedir duplicatas no mesmo diretório (case-insensitive),
    # exceto o próprio
    if File.objects.filter(
        uploader=request.user,
        folder=file.folder,
        name__iexact=new_name,
    ).exclude(id=file.id).exists():
        messages.error(
            request, "Já existe um arquivo com esse nome neste diretório."
        )
        return redirect(next_url)

    file.name = new_name
    file.save()
    messages.success(request, f"Arquivo renomeado para '{new_name}'.")
    return redirect(next_url)


def _is_descendant(folder, potential_parent):
    """
    Helper para evitar mover uma pasta para ela mesma ou seus filhos.
    """
    current = potential_parent
    while current:
        if current == folder:
            return True
        current = current.parent
    return False


@login_required(login_url="/")
def move_item(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido."}, status=405)

    item_type = request.POST.get("item_type")
    item_id = request.POST.get("item_id")
    target_folder_id = request.POST.get("target_folder") or None

    if not item_type or not item_id:
        return JsonResponse(
            {"error": "Dados insuficientes para mover o item."}, status=400
        )

    target_folder = None
    if target_folder_id:
        target_folder = get_object_or_404(
            Folder,
            id=target_folder_id,
            owner=request.user,
            is_deleted=False,
        )

    if item_type == "folder":
        folder = get_object_or_404(
            Folder,
            id=item_id,
            owner=request.user,
            is_deleted=False,
        )

        if target_folder and _is_descendant(folder, target_folder):
            error_message = (
                "Não é possível mover a pasta para dentro dela mesma."
            )
            return JsonResponse(
                {"error": error_message},
                status=400,
            )

        folder.parent = target_folder
        folder.save()
        return JsonResponse({"success": True})

    elif item_type == "file":
        file = get_object_or_404(
            File,
            id=item_id,
            uploader=request.user,
            is_deleted=False,
        )
        file.folder = target_folder
        file.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Tipo de item inválido."}, status=400)
