from django.urls import path

from .views import create_folder, upload_file, workspace_home

urlpatterns = [
    path(route="workspace", view=workspace_home, name="workspace_home"),
    path(route="create-folder/", view=create_folder, name="create_folder"),
    path(route="upload-file/", view=upload_file, name="upload_file"),
]
