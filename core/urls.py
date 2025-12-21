"""
Configuração de URLs do projeto.

Este arquivo define as rotas principais da aplicação e inclui
as URLs dos apps instalados.
"""
from django.contrib import admin
from django.urls import include, path

# ============================================================================
# PADRÕES DE URL DO PROJETO
# ============================================================================

urlpatterns = [
    # Interface administrativa do Django
    path("admin/", admin.site.urls),

    # URLs do django-allauth (autenticação e login social)
    path("accounts/", include("allauth.urls")),

    # URLs do app de usuários
    path("", include("users.urls")),

    # URLs do app de workspace
    path("", include("workspace.urls")),
]
