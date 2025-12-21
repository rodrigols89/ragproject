"""
Configuração de URLs do app workspace.

Este módulo define todas as rotas relacionadas ao gerenciamento
de pastas e arquivos no workspace.
"""
from django.urls import path

from . import views

# Padrões de URL do workspace
urlpatterns = [
    # Página principal do workspace
    path(
        route="workspace",
        view=views.workspace_home,
        name="workspace_home"
    ),

    # Criação de pasta
    path(
        route="create-folder/",
        view=views.create_folder,
        name="create_folder"
    ),

    # Upload de arquivo
    path(
        route="upload-file/",
        view=views.upload_file,
        name="upload_file"
    ),

    # Exclusão de pasta
    path(
        route="delete-folder/<int:folder_id>/",
        view=views.delete_folder,
        name="delete_folder"
    ),

    # Exclusão de arquivo
    path(
        route="delete-file/<int:file_id>/",
        view=views.delete_file,
        name="delete_file"
    ),

    # Renomeação de pasta
    path(
        route="rename-folder/<int:folder_id>/",
        view=views.rename_folder,
        name="rename_folder"
    ),

    # Renomeação de arquivo
    path(
        route="rename-file/<int:file_id>/",
        view=views.rename_file,
        name="rename_file"
    ),

    # Movimentação de item (pasta ou arquivo)
    path(
        route="move-item/",
        view=views.move_item,
        name="move_item"
    ),
]
