import json
import logging
import os
import traceback
from collections import Counter
from dataclasses import dataclass

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FolderForm
from .models import File, Folder
from .validators import validate_file

MAX_ERROR_MESSAGES_UPLOAD_FILE = 3
MAX_ERROR_MESSAGES_UPLOAD_FOLDER = 5


@dataclass
class FolderUploadParams:
    """Parâmetros para processamento de upload de pasta."""
    user: object
    uploaded_files: list
    file_paths_list: list
    folder_name: str
    main_folder: object
    folders_cache: dict


@dataclass
class FileUploadParams:
    """Parâmetros para processamento de upload de arquivo."""
    user: object
    uploaded_file: object
    file_path: str
    folder_name: str
    target_folder: object
    folders_cache: dict


@dataclass
class UploadResults:
    """Resultados do upload de pasta."""
    request: object
    main_folder: object
    folder_name: str
    uploaded_count: int
    error_count: int
    error_messages: list


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


def _determine_folder_name(uploaded_files, folder_name):
    """
    Determina o nome da pasta a partir dos arquivos ou nome fornecido.
    """
    if folder_name:
        return folder_name

    first_dirs = []
    for uploaded_file in uploaded_files:
        file_path = uploaded_file.name
        path_parts = file_path.split("/")
        if len(path_parts) > 1 and path_parts[0].strip():
            first_dirs.append(path_parts[0].strip())

    if not first_dirs:
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        return f"Pasta Upload {timestamp}"

    unique_first_dirs = set(first_dirs)
    if len(unique_first_dirs) == 1:
        return list(unique_first_dirs)[0]

    if len(unique_first_dirs) > 1:
        dir_counter = Counter(first_dirs)
        return dir_counter.most_common(1)[0][0]

    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    return f"Pasta Upload {timestamp}"


def _ensure_unique_folder_name(user, parent_folder, folder_name):
    """
    Garante que o nome da pasta seja único no mesmo nível hierárquico.
    """
    if not Folder.objects.filter(
        owner=user,
        parent=parent_folder,
        name__iexact=folder_name,
        is_deleted=False
    ).exists():
        return folder_name

    base_name = folder_name
    counter = 1
    while Folder.objects.filter(
        owner=user,
        parent=parent_folder,
        name__iexact=folder_name,
        is_deleted=False
    ).exists():
        folder_name = f"{base_name} ({counter})"
        counter += 1

    return folder_name


def _setup_folder_upload(user, uploaded_files, folder_name_input,
                         parent_folder):
    """
    Configura o upload de pasta: determina nome e cria pasta principal.
    Retorna (main_folder, folder_name).
    """
    folder_name = _determine_folder_name(uploaded_files, folder_name_input)
    folder_name = _ensure_unique_folder_name(
        user, parent_folder, folder_name
    )

    main_folder = Folder.objects.create(
        name=folder_name,
        owner=user,
        parent=parent_folder
    )

    return (main_folder, folder_name)


def _prepare_file_paths(uploaded_files, file_paths_json):
    """
    Prepara a lista de caminhos de arquivos a partir dos arquivos
    enviados e do JSON opcional.
    """

    file_paths_list = []

    if file_paths_json:
        try:
            file_paths_list = json.loads(file_paths_json)
        except json.JSONDecodeError:
            pass

    if not file_paths_list:
        file_paths_list = [
            uploaded_file.name for uploaded_file in uploaded_files
        ]

    return file_paths_list


def _normalize_path_parts(file_path, folder_name):
    """
    Normaliza os path_parts removendo o primeiro diretório se for igual ao
    folder_name.
    """
    path_parts = file_path.split("/")
    if len(path_parts) > 1:
        first_dir = path_parts[0].strip()
        if (folder_name and
                first_dir.lower() == folder_name.strip().lower()):
            path_parts = path_parts[1:]
    return path_parts


def _collect_folder_paths(file_paths_list, folder_name):
    """
    Coleta todos os caminhos de pastas a partir dos caminhos dos arquivos.
    """
    all_folder_paths = set()
    for file_path in file_paths_list:
        if not file_path:
            continue

        path_parts = _normalize_path_parts(file_path, folder_name)
        if len(path_parts) <= 1:
            continue

        folder_path = "/".join(path_parts[:-1])
        if not folder_path or not folder_path.strip():
            continue

        all_folder_paths.add(folder_path.strip())
        path_components = folder_path.split("/")
        for i in range(1, len(path_components) + 1):
            intermediate_path = "/".join(path_components[:i])
            if intermediate_path and intermediate_path.strip():
                all_folder_paths.add(intermediate_path.strip())

    return sorted(all_folder_paths, key=lambda x: (x.count("/"), x))


def _create_subfolders(user, main_folder, sorted_paths):
    """
    Cria todas as subpastas necessárias e retorna um cache de pastas.
    """
    folders_cache = {}
    folders_cache[""] = main_folder

    for folder_path in sorted_paths:
        if folder_path in folders_cache:
            continue

        current_path = ""
        current_parent = main_folder

        for raw_subfolder_name in folder_path.split("/"):
            cleaned_name = raw_subfolder_name.strip()
            if not cleaned_name:
                continue

            if current_path:
                current_path = f"{current_path}/{cleaned_name}"
            else:
                current_path = cleaned_name

            if current_path in folders_cache:
                current_parent = folders_cache[current_path]
                continue

            existing_folder = Folder.objects.filter(
                owner=user,
                parent=current_parent,
                name=cleaned_name,
                is_deleted=False
            ).first()

            if existing_folder:
                folders_cache[current_path] = existing_folder
                current_parent = existing_folder
            else:
                new_folder = Folder.objects.create(
                    name=cleaned_name,
                    owner=user,
                    parent=current_parent
                )
                folders_cache[current_path] = new_folder
                current_parent = new_folder

    return folders_cache


def _get_target_folder(user, main_folder, path_parts, folders_cache):
    """
    Obtém a pasta de destino para um arquivo baseado em seu caminho.
    """
    if len(path_parts) <= 1:
        return main_folder

    folder_path = "/".join(path_parts[:-1])
    if not folder_path or not folder_path.strip():
        return main_folder

    folder_path_stripped = folder_path.strip()
    if folder_path_stripped in folders_cache:
        return folders_cache[folder_path_stripped]

    path_components = folder_path_stripped.split("/")
    current_parent = main_folder
    for subfolder_name in path_components:
        if not subfolder_name:
            continue
        existing_folder = Folder.objects.filter(
            owner=user,
            parent=current_parent,
            name=subfolder_name,
            is_deleted=False
        ).first()
        if existing_folder:
            current_parent = existing_folder
        else:
            break

    return current_parent


def _extract_error_message(exception):
    """
    Extrai a mensagem de erro de uma exceção.
    """
    if isinstance(exception, ValidationError):
        if hasattr(exception, 'messages') and exception.messages:
            return str(exception.messages[0])
        if hasattr(exception, 'message'):
            return str(exception.message)
        return str(exception)

    if hasattr(exception, 'message'):
        return str(exception.message)

    return str(exception)


def _extract_error_detail(exception):
    """
    Extrai detalhes de erro de uma exceção para logging.
    """
    error_detail = str(exception)
    if isinstance(exception, ValidationError):
        if hasattr(exception, 'messages') and exception.messages:
            error_detail = str(exception.messages[0])
        elif hasattr(exception, 'message_dict'):
            error_detail = str(exception.message_dict)
    return error_detail


def _process_file_upload(params: FileUploadParams):
    """
    Processa o upload de um arquivo individual.
    Retorna (success, error_message, file_name).
    """
    if not params.file_path:
        params.file_path = params.uploaded_file.name

    path_parts = _normalize_path_parts(
        params.file_path, params.folder_name
    )
    file_name = path_parts[-1]

    target_folder = _get_target_folder(
        params.user, params.target_folder, path_parts, params.folders_cache
    )

    try:
        validate_file(params.uploaded_file)
    except Exception as e:
        error_message = _extract_error_message(e)
        return (False, error_message, file_name)

    base, ext = os.path.splitext(file_name)
    new_name = file_name
    counter = 1

    while File.objects.filter(
        uploader=params.user,
        folder=target_folder,
        name__iexact=new_name,
        is_deleted=False
    ).exists():
        new_name = f"{base} ({counter}){ext}"
        counter += 1

    try:
        File.objects.create(
            name=new_name,
            file=params.uploaded_file,
            folder=target_folder,
            uploader=params.user,
        )
        return (True, None, file_name)
    except Exception as e:
        error_detail = _extract_error_detail(e)
        if settings.DEBUG:
            logger = logging.getLogger(__name__)
            logger.error(
                f"Erro ao salvar arquivo {file_name}: {error_detail}"
            )
            logger.error(traceback.format_exc())
        error_message = (
            f"{file_name}: Erro ao salvar arquivo - {error_detail}"
        )
        return (False, error_message, file_name)


def _process_folder_uploads(params: FolderUploadParams):
    """
    Processa todos os uploads de arquivos em uma pasta.
    Retorna (uploaded_count, error_count, error_messages).
    """
    files_with_paths = []
    for i, uploaded_file in enumerate(params.uploaded_files):
        file_path = (
            params.file_paths_list[i]
            if i < len(params.file_paths_list)
            else uploaded_file.name
        )
        files_with_paths.append((uploaded_file, file_path))

    uploaded_count = 0
    error_count = 0
    error_messages = []

    for uploaded_file, file_path in files_with_paths:
        file_params = FileUploadParams(
            user=params.user,
            uploaded_file=uploaded_file,
            file_path=file_path,
            folder_name=params.folder_name,
            target_folder=params.main_folder,
            folders_cache=params.folders_cache
        )
        success, error_message, file_name = _process_file_upload(
            file_params
        )

        if success:
            uploaded_count += 1
        else:
            error_count += 1
            error_messages.append(error_message)

    return (uploaded_count, error_count, error_messages)


def _process_folder_upload_complete(user, uploaded_files, file_paths_json,
                                     folder_name, main_folder):
    """
    Processa completamente o upload de pasta: cria subpastas e arquivos.
    Retorna (uploaded_count, error_count, error_messages).
    """
    file_paths_list = _prepare_file_paths(uploaded_files, file_paths_json)
    sorted_paths = _collect_folder_paths(file_paths_list, folder_name)
    folders_cache = _create_subfolders(
        user, main_folder, sorted_paths
    )

    folder_params = FolderUploadParams(
        user=user,
        uploaded_files=uploaded_files,
        file_paths_list=file_paths_list,
        folder_name=folder_name,
        main_folder=main_folder,
        folders_cache=folders_cache
    )

    return _process_folder_uploads(folder_params)


def _handle_upload_results(results: UploadResults):
    """
    Processa os resultados do upload e exibe mensagens apropriadas.
    """
    if results.uploaded_count == 0 and results.error_count > 0:
        results.main_folder.delete()
        max_errors = MAX_ERROR_MESSAGES_UPLOAD_FOLDER
        for error_msg in results.error_messages[:max_errors]:
            messages.error(results.request, error_msg)
        if len(results.error_messages) > max_errors:
            remaining = len(results.error_messages) - max_errors
            messages.warning(
                results.request,
                f"E mais {remaining} arquivo(s) com erro."
            )
    elif results.error_count == 0 and results.uploaded_count > 0:
        messages.success(
            results.request,
            f"Pasta '{results.folder_name}' uploaded com sucesso!"
        )
    elif results.uploaded_count > 0 and results.error_count > 0:
        max_errors = MAX_ERROR_MESSAGES_UPLOAD_FOLDER
        for error_msg in results.error_messages[:max_errors]:
            messages.error(results.request, error_msg)
        if len(results.error_messages) > max_errors:
            remaining = len(results.error_messages) - max_errors
            messages.warning(
                results.request,
                f"E mais {remaining} arquivo(s) com erro."
            )
    else:
        results.main_folder.delete()
        messages.error(results.request, "Nenhum arquivo foi processado.")


@login_required(login_url="/")
def upload_folder(request):
    """
    View para upload de pastas inteiras.

    Cria a pasta principal e todas as subpastas detectadas.
    Não processa arquivos.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Redireciona após criar as pastas
    """
    if request.method != "POST":
        return redirect("workspace_home")

    uploaded_files = request.FILES.getlist("files")
    next_url = request.POST.get("next", "workspace_home")
    folder_id = request.POST.get("folder")
    parent_folder = None

    if folder_id:
        parent_folder = get_object_or_404(
            Folder,
            id=folder_id,
            owner=request.user
        )

    if not uploaded_files:
        messages.error(request, "Nenhuma pasta foi selecionada.")
        return redirect(next_url)

    folder_name_input = request.POST.get("folder_name", "").strip()
    main_folder, folder_name = _setup_folder_upload(
        request.user, uploaded_files, folder_name_input, parent_folder
    )

    file_paths_json = request.POST.get("file_paths", "")
    uploaded_count, error_count, error_messages = (
        _process_folder_upload_complete(
            request.user,
            uploaded_files,
            file_paths_json,
            folder_name,
            main_folder
        )
    )

    results = UploadResults(
        request=request,
        main_folder=main_folder,
        folder_name=folder_name,
        uploaded_count=uploaded_count,
        error_count=error_count,
        error_messages=error_messages
    )
    _handle_upload_results(results)

    return redirect(next_url)


@login_required(login_url="/")
def delete_file(request, file_id):
    """
    View para exclusão de arquivo (soft delete).

    Marca o arquivo como deletado sem removê-lo fisicamente do banco.
    Retorna para a pasta onde estava ou para a raiz.

    Args:
        request: Objeto HttpRequest do Django
        file_id: ID do arquivo a ser deletado

    Returns:
        HttpResponseRedirect: Redireciona após exclusão
    """
    file = get_object_or_404(
        File,
        id=file_id,
        uploader=request.user
    )

    folder = file.folder

    file.is_deleted = True
    file.deleted_at = timezone.now()
    file.save()

    messages.success(
        request,
        f"Arquivo '{file.name}' movido para a lixeira."
    )

    if folder:
        return redirect(f"/workspace?folder={folder.id}")

    return redirect("workspace_home")
