import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
        folders = Folder.objects.filter(parent=current_folder)

        # Arquivos da pasta atual
        files = File.objects.filter(folder=current_folder)

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
            owner=request.user, parent__isnull=True
        )

        files = File.objects.filter(uploader=request.user, folder__isnull=True)

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
                return redirect(request.POST.get("next", "workspace"))

        # ---------------------------------------------------------------
        # ❗ Se houver erro, renderizar novamente a página CORRETAMENTE
        # mantendo arquivos e pastas da pasta atual (ou raiz)
        # ---------------------------------------------------------------

        # Pastas da pasta atual (ou raiz)
        folders = Folder.objects.filter(
            parent=parent_folder, owner=request.user
        )

        # Arquivos da pasta atual (ou raiz)
        files = File.objects.filter(
            folder=parent_folder, uploader=request.user
        )

        # Breadcrumbs corretos
        breadcrumbs = build_breadcrumbs(parent_folder)

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
    return redirect("workspace")

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
