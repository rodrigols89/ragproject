"""
Configuração de URLs do projeto.

Este arquivo define as rotas principais da aplicação e inclui
as URLs dos apps instalados.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("", include("workspace.urls")),
]
