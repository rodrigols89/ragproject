"""
Views do app workspace.

Este módulo contém todas as views relacionadas ao gerenciamento
de pastas e arquivos no workspace, incluindo CRUD completo e
operações de movimentação.
"""
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FolderForm
from .models import File, Folder
from .validators import validate_file

# ============================================================================
# VIEWS DE NAVEGAÇÃO E LISTAGEM
# ============================================================================


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

    # Se o usuário clicou em alguma pasta específica
    if folder_id:
        # Busca a pasta atual (garante que pertence ao usuário)
        current_folder = get_object_or_404(
            Folder,
            id=folder_id,
            owner=request.user
        )

        # Busca subpastas da pasta atual (não deletadas)
        folders = Folder.objects.filter(
            parent=current_folder,
            is_deleted=False
        )

        # Busca arquivos da pasta atual (não deletados)
        files = File.objects.filter(
            folder=current_folder,
            is_deleted=False
        )

        # Constrói breadcrumbs (caminho completo até a raiz)
        breadcrumbs = []
        temp = current_folder
        while temp:
            breadcrumbs.append(temp)
            temp = temp.parent
        breadcrumbs.reverse()

    else:
        # Estamos no nível raiz (sem pasta selecionada)
        current_folder = None

        # Pastas da raiz (sem pai, não deletadas)
        folders = Folder.objects.filter(
            owner=request.user,
            parent__isnull=True,
            is_deleted=False
        )

        # Arquivos da raiz (sem pasta, não deletados)
        files = File.objects.filter(
            uploader=request.user,
            folder__isnull=True,
            is_deleted=False
        )

        breadcrumbs = []  # Raiz não tem caminho

    # Contexto passado para o template
    context = {
        "current_folder": current_folder,
        "folders": folders,
        "files": files,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "pages/workspace_home.html", context)


# ============================================================================
# VIEWS DE CRIAÇÃO
# ============================================================================

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

        # Obtém a pasta pai (se aplicável)
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

            # Verifica duplicação (ignorando maiúsculas/minúsculas)
            # no mesmo nível hierárquico
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
                # Cria nova pasta
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

        # Se houver erros, reexibe o formulário com contexto
        if parent_folder:
            # Estamos dentro de uma pasta
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
            # Estamos na raiz
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
            "show_modal": True,  # Reabre modal com erro
        }

        return render(request, "pages/workspace_home.html", context)

    # Se método não for POST, redireciona para a home
    return redirect("workspace_home")


@login_required(login_url="/")
def upload_file(request):
    """
    View para upload de arquivos.

    Realiza validações de extensão e tamanho, além de renomear
    automaticamente arquivos duplicados.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Redireciona após upload ou exibe erros
    """
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        next_url = request.POST.get("next", "workspace_home")
        folder_id = request.POST.get("folder")
        folder = None

        # Obtém pasta atual se existir
        if folder_id:
            folder = get_object_or_404(
                Folder,
                id=folder_id,
                owner=request.user
            )

        # Verifica se algum arquivo foi enviado
        if not uploaded_file:
            messages.error(request, "Nenhum arquivo foi enviado.")
            return redirect(next_url)

        # Validações via validators.py
        try:
            validate_file(uploaded_file)
        except Exception as e:
            # Captura mensagem de erro da validação
            messages.error(request, e.message)
            return redirect(next_url)

        # Renome automático em caso de duplicação
        original_name = uploaded_file.name
        base, ext = os.path.splitext(original_name)
        new_name = original_name
        counter = 1

        # Incrementa contador até encontrar nome único
        while File.objects.filter(
            uploader=request.user,
            folder=folder,
            name__iexact=new_name,
            is_deleted=False
        ).exists():
            new_name = f"{base} ({counter}){ext}"
            counter += 1

        # Criação do arquivo no banco de dados
        File.objects.create(
            name=new_name,
            file=uploaded_file,
            folder=folder,
            uploader=request.user,
        )

        messages.success(
            request,
            f"Arquivo '{new_name}' enviado com sucesso!"
        )
        return redirect(next_url)

    return redirect("workspace_home")


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

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


# ============================================================================
# VIEWS DE EXCLUSÃO (SOFT DELETE)
# ============================================================================

@login_required(login_url="/")
def delete_folder(request, folder_id):
    """
    View para exclusão de pasta (soft delete).

    Marca a pasta como deletada sem removê-la fisicamente do banco.
    Retorna para a pasta pai ou para a raiz.

    Args:
        request: Objeto HttpRequest do Django
        folder_id: ID da pasta a ser deletada

    Returns:
        HttpResponseRedirect: Redireciona após exclusão
    """
    folder = get_object_or_404(
        Folder,
        id=folder_id,
        owner=request.user
    )

    # Pasta pai para retornar após exclusão
    parent = folder.parent

    # Soft delete: marca como deletado
    folder.is_deleted = True
    folder.deleted_at = timezone.now()
    folder.save()

    messages.success(
        request,
        f"Pasta '{folder.name}' movida para a lixeira."
    )

    # Retorna para pasta pai ou raiz
    if parent:
        return redirect(f"/workspace?folder={parent.id}")

    return redirect("workspace_home")


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

    # Pasta onde o arquivo estava
    folder = file.folder

    # Soft delete: marca como deletado
    file.is_deleted = True
    file.deleted_at = timezone.now()
    file.save()

    messages.success(
        request,
        f"Arquivo '{file.name}' movido para a lixeira."
    )

    # Retorna para pasta ou raiz
    if folder:
        return redirect(f"/workspace?folder={folder.id}")

    return redirect("workspace_home")


# ============================================================================
# VIEWS DE RENOMEAÇÃO
# ============================================================================

@login_required(login_url="/")
def rename_folder(request, folder_id):
    """
    View para renomear pasta.

    Valida o novo nome e verifica duplicação no mesmo nível hierárquico.

    Args:
        request: Objeto HttpRequest do Django
        folder_id: ID da pasta a ser renomeada

    Returns:
        HttpResponseRedirect: Redireciona após renomeação
    """
    folder = get_object_or_404(
        Folder,
        id=folder_id,
        owner=request.user,
        is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    # Valida nome não vazio
    if not new_name:
        messages.error(
            request,
            "O nome da pasta não pode ser vazio."
        )
        return redirect(next_url)

    # Impede duplicatas no mesmo parent (case-insensitive),
    # exceto a própria pasta
    if Folder.objects.filter(
        owner=request.user,
        parent=folder.parent,
        name__iexact=new_name,
        is_deleted=False,
    ).exclude(id=folder.id).exists():
        messages.error(
            request,
            "Já existe uma pasta com esse nome nesse diretório."
        )
        return redirect(next_url)

    # Atualiza nome e salva
    folder.name = new_name
    folder.save()
    messages.success(
        request,
        f"Pasta renomeada para '{new_name}'."
    )
    return redirect(next_url)


@login_required(login_url="/")
def rename_file(request, file_id):
    """
    View para renomear arquivo.

    Valida o novo nome e verifica duplicação no mesmo diretório.

    Args:
        request: Objeto HttpRequest do Django
        file_id: ID do arquivo a ser renomeado

    Returns:
        HttpResponseRedirect: Redireciona após renomeação
    """
    file = get_object_or_404(
        File,
        id=file_id,
        uploader=request.user,
        is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    # Valida nome não vazio
    if not new_name:
        messages.error(
            request,
            "O nome do arquivo não pode ser vazio."
        )
        return redirect(next_url)

    # Impede duplicatas no mesmo diretório (case-insensitive),
    # exceto o próprio arquivo
    if File.objects.filter(
        uploader=request.user,
        folder=file.folder,
        name__iexact=new_name,
        is_deleted=False,
    ).exclude(id=file.id).exists():
        messages.error(
            request,
            "Já existe um arquivo com esse nome neste diretório."
        )
        return redirect(next_url)

    # Atualiza nome e salva
    file.name = new_name
    file.save()
    messages.success(
        request,
        f"Arquivo renomeado para '{new_name}'."
    )
    return redirect(next_url)


# ============================================================================
# VIEWS DE MOVIMENTAÇÃO
# ============================================================================

def _is_descendant(folder, potential_parent):
    """
    Helper para evitar mover uma pasta para ela mesma ou seus filhos.

    Verifica se a pasta potencial pai é descendente da pasta atual,
    o que criaria um ciclo na hierarquia.

    Args:
        folder: Pasta que está sendo movida
        potential_parent: Pasta que seria o novo pai

    Returns:
        bool: True se potential_parent é descendente de folder
    """
    current = potential_parent
    while current:
        if current == folder:
            return True
        current = current.parent
    return False


@login_required(login_url="/")
def move_item(request):
    """
    View para mover pastas ou arquivos (via AJAX).

    Suporta mover itens entre pastas ou para a raiz.
    Retorna JSON para requisições AJAX.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        JsonResponse: Resposta JSON com sucesso ou erro
    """
    if request.method != "POST":
        return JsonResponse(
            {"error": "Método inválido."},
            status=405
        )

    # Extrai dados da requisição
    item_type = request.POST.get("item_type")
    item_id = request.POST.get("item_id")
    target_folder_id = request.POST.get("target_folder") or None

    # Valida dados mínimos
    if not item_type or not item_id:
        return JsonResponse(
            {"error": "Dados insuficientes para mover o item."},
            status=400
        )

    # Obtém pasta destino (None = raiz)
    target_folder = None
    if target_folder_id:
        target_folder = get_object_or_404(
            Folder,
            id=target_folder_id,
            owner=request.user,
            is_deleted=False,
        )

    # Processa movimentação de pasta
    if item_type == "folder":
        folder = get_object_or_404(
            Folder,
            id=item_id,
            owner=request.user,
            is_deleted=False,
        )

        # Evita mover pasta para dentro dela mesma ou seus filhos
        if target_folder and _is_descendant(folder, target_folder):
            error_message = (
                "Não é possível mover a pasta para dentro dela mesma."
            )
            return JsonResponse(
                {"error": error_message},
                status=400,
            )

        # Atualiza parent e salva
        folder.parent = target_folder
        folder.save()
        return JsonResponse({"success": True})

    # Processa movimentação de arquivo
    elif item_type == "file":
        file = get_object_or_404(
            File,
            id=item_id,
            uploader=request.user,
            is_deleted=False,
        )
        # Atualiza pasta e salva
        file.folder = target_folder
        file.save()
        return JsonResponse({"success": True})

    # Tipo de item inválido
    return JsonResponse(
        {"error": "Tipo de item inválido."},
        status=400
    )
