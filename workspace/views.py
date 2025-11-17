from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FolderForm
from .models import File, Folder


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

        # Se houver erro, renderizar novamente o template para exibir mensagens
        context = {
            "form": form,
            "current_folder": parent_folder,
            "folders": Folder.objects.filter(
                parent=parent_folder, owner=request.user
            ),
            "files": [],  # se tiver Files também adicione
            "breadcrumbs": [],  # se quiser breadcrumbs no erro
            "show_modal": True,  # reabrir modal com erro
        }
        return render(request, "pages/workspace_home.html", context)

    # Se método não for POST, redireciona para a home
    return redirect("workspace")
