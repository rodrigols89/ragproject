from django.urls import path

from .views import workspace_home

urlpatterns = [
    path(route="workspace", view=workspace_home, name="workspace_home"),
]
