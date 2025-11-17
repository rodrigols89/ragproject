from django.urls import path

from .views import create_folder, workspace_home

urlpatterns = [
    path(route="workspace", view=workspace_home, name="workspace_home"),
    path("create-folder/", create_folder, name="create_folder"),
]
