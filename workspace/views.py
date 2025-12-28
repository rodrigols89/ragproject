import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FolderForm
from .models import File, Folder
from .validators import validate_file

MAX_ERROR_MESSAGES_UPLOAD_FILE = 3
MAX_ERROR_MESSAGES_UPLOAD_FOLDER = 5


@login_required(login_url="/")
def workspace_home(request):
    """
    View principal do workspace.

    Exibe as pastas e arquivos do usuário, suportando navegação
    hierárquica através do parâmetro 'folder' na query string.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Renderiza o template workspace_home.html
    """
    folder_id = request.GET.get("folder")

    if folder_id:
        current_folder = get_object_or_404(
            Folder,
            id=folder_id,
            owner=request.user
        )

        folders = Folder.objects.filter(
            parent=current_folder,
            owner=request.user,
            is_deleted=False
        ).order_by("name")

        files = File.objects.filter(
            folder=current_folder,
            uploader=request.user,
            is_deleted=False
        ).order_by("name")

        breadcrumbs = []
        temp = current_folder
        while temp:
            breadcrumbs.append(temp)
            temp = temp.parent
        breadcrumbs.reverse()

    else:
        current_folder = None

        folders = Folder.objects.filter(
            owner=request.user,
            parent__isnull=True,
            is_deleted=False
        ).order_by("name")

        files = File.objects.filter(
            uploader=request.user,
            folder__isnull=True,
            is_deleted=False
        ).order_by("name")

        breadcrumbs = []

    context = {
        "current_folder": current_folder,
        "folders": folders,
        "files": files,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "pages/workspace_home.html", context)


def build_breadcrumbs(folder):
    """
    Constrói a lista de breadcrumbs (caminho completo).

    Percorre a hierarquia de pastas desde a pasta atual até a raiz,
    construindo uma lista ordenada do caminho completo.

    Args:
        folder: Instância de Folder para construir o caminho

    Returns:
        list: Lista de pastas do caminho (raiz -> atual)
    """
    breadcrumbs = []
    while folder:
        breadcrumbs.insert(0, folder)
        folder = folder.parent
    return breadcrumbs


@login_required(login_url="/")
def create_folder(request):
    """
    View para criação de nova pasta.

    Valida o nome e verifica duplicação no mesmo nível hierárquico.
    Suporta criação de pastas dentro de outras pastas.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Redireciona ou renderiza template com erros
    """
    if request.method == "POST":
        form = FolderForm(request.POST)

        parent_id = request.POST.get("parent")
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(
                Folder,
                id=parent_id,
                owner=request.user
            )

        if form.is_valid():
            name = form.cleaned_data["name"]

            if Folder.objects.filter(
                owner=request.user,
                name__iexact=name,
                parent=parent_folder,
                is_deleted=False
            ).exists():
                form.add_error(
                    "name",
                    "Já existe uma pasta com esse nome nesse diretório."
                )
            else:
                new_folder = form.save(commit=False)
                new_folder.owner = request.user
                new_folder.parent = parent_folder
                new_folder.save()

                messages.success(
                    request,
                    f"Pasta '{name}' criada com sucesso!"
                )
                return redirect(
                    request.POST.get("next", "workspace_home")
                )

        if parent_folder:
            folders = Folder.objects.filter(
                parent=parent_folder,
                is_deleted=False
            )
            files = File.objects.filter(
                folder=parent_folder,
                is_deleted=False
            )
            breadcrumbs = build_breadcrumbs(parent_folder)
        else:
            folders = Folder.objects.filter(
                owner=request.user,
                parent__isnull=True,
                is_deleted=False
            )
            files = File.objects.filter(
                uploader=request.user,
                folder__isnull=True,
                is_deleted=False
            )
            breadcrumbs = []

        context = {
            "form": form,
            "current_folder": parent_folder,
            "folders": folders,
            "files": files,
            "breadcrumbs": breadcrumbs,
            "show_modal": True,
        }

        return render(request, "pages/workspace_home.html", context)

    return redirect("workspace_home")


def _validate_uploaded_file(uploaded_file):
    """
    Valida um arquivo enviado e retorna mensagem de erro se houver.
    """
    try:
        validate_file(uploaded_file)
        return None
    except Exception as e:
        if hasattr(e, '__str__'):
            error_message = str(e)
        else:
            error_message = getattr(e, 'message', 'Erro desconhecido')
        return f"{uploaded_file.name}: {error_message}"


def _generate_unique_filename(user, folder, original_name):
    """
    Gera um nome de arquivo único para evitar duplicatas.
    """
    base, ext = os.path.splitext(original_name)
    new_name = original_name
    counter = 1

    while File.objects.filter(
        uploader=user,
        folder=folder,
        name__iexact=new_name,
        is_deleted=False
    ).exists():
        new_name = f"{base} ({counter}){ext}"
        counter += 1

    return new_name


def _create_file_instance(user, folder, uploaded_file, new_name):
    """
    Cria uma instância de File no banco de dados.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        File.objects.create(
            name=new_name,
            file=uploaded_file,
            folder=folder,
            uploader=user,
        )
        return True
    except Exception:
        return False


def _process_single_file_upload(user, folder, uploaded_file):
    """
    Processa o upload de um único arquivo.
    Retorna (success, error_message).
    """
    error_msg = _validate_uploaded_file(uploaded_file)
    if error_msg:
        return (False, error_msg)

    new_name = _generate_unique_filename(
        user, folder, uploaded_file.name
    )

    if _create_file_instance(user, folder, uploaded_file, new_name):
        return (True, None)

    return (False, f"{uploaded_file.name}: Erro ao salvar arquivo")


@login_required(login_url="/")
def upload_file(request):
    """
    View para upload de arquivos (um ou múltiplos).

    Realiza validações de extensão e tamanho, além de renomear
    automaticamente arquivos duplicados. Suporta upload de
    um ou múltiplos arquivos.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Redireciona após upload ou exibe erros
    """
    if request.method == "POST":
        uploaded_files = request.FILES.getlist("file")
        next_url = request.POST.get("next", "workspace_home")
        folder_id = request.POST.get("folder")
        folder = None

        if folder_id:
            folder = get_object_or_404(
                Folder,
                id=folder_id,
                owner=request.user
            )

        if not uploaded_files:
            messages.error(request, "Nenhum arquivo foi enviado.")
            return redirect(next_url)

        uploaded_count = 0
        error_count = 0
        error_messages = []

        for uploaded_file in uploaded_files:
            success, error_message = _process_single_file_upload(
                request.user, folder, uploaded_file
            )

            if success:
                uploaded_count += 1
            else:
                error_count += 1
                error_messages.append(error_message)

        if uploaded_count > 0:
            if uploaded_count == 1:
                messages.success(
                    request,
                    "Arquivo enviado com sucesso!"
                )
            else:
                messages.success(
                    request,
                    f"{uploaded_count} arquivo(s) enviado(s) com sucesso!"
                )

        if error_count > 0:
            for error_msg in error_messages[:MAX_ERROR_MESSAGES_UPLOAD_FILE]:
                messages.error(request, error_msg)
            if len(error_messages) > MAX_ERROR_MESSAGES_UPLOAD_FILE:
                max_err = MAX_ERROR_MESSAGES_UPLOAD_FILE
                remaining = len(error_messages) - max_err
                messages.warning(
                    request,
                    f"E mais {remaining} arquivo(s) com erro."
                )

        return redirect(next_url)

    return redirect("workspace_home")
