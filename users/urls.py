"""
Configuração de URLs da aplicação 'users'.

Este módulo define todas as rotas relacionadas à autenticação
e gerenciamento de usuários, incluindo login, logout, criação
de conta e página inicial.
"""
from django.urls import path

from .views import create_account, home_view, login_view, logout_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(route="home/", view=home_view, name="home"),
    path(route="logout/", view=logout_view, name="logout"),
    path(
        route="create-account/",
        view=create_account,
        name="create-account"
    ),
]
