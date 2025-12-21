"""
Configuração de URLs da aplicação 'users'.

Este módulo define todas as rotas relacionadas à autenticação
e gerenciamento de usuários, incluindo login, logout, criação
de conta e página inicial.
"""
from django.urls import path

from .views import create_account, home_view, login_view, logout_view

# ============================================================================
# PADRÕES DE URL DA APLICAÇÃO USERS
# ============================================================================

urlpatterns = [
    # Página inicial (login)
    # Rota raiz que exibe o formulário de login
    path(route="", view=login_view, name="index"),

    # Página home (área logada)
    # Requer autenticação para acessar
    path(route="home/", view=home_view, name="home"),

    # Logout
    # Encerra a sessão do usuário e redireciona para login
    path(route="logout/", view=logout_view, name="logout"),

    # Criar conta
    # Formulário de cadastro de novos usuários
    path(
        route="create-account/",
        view=create_account,
        name="create-account"
    ),
]
