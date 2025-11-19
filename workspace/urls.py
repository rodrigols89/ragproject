from django.urls import path

from . import views

urlpatterns = [
    path(route="workspace", view=views.workspace_home, name="workspace_home"),
    path(route="create-folder/", view=views.create_folder, name="create_folder"),
    path(route="upload-file/", view=views.upload_file, name="upload_file"),
    path(route="delete-folder/<int:folder_id>/", view=views.delete_folder, name="delete_folder"),
    path(route="delete-file/<int:file_id>/", view=views.delete_file, name="delete_file"),
]
