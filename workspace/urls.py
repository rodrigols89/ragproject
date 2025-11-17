from django.urls import path

from .views import workspace_home

urlpatterns = [
    path(route="workspace_home", view=workspace_home, name="workspace_home"),
]
