"""
Views da aplicação 'users'.

Este módulo contém todas as views relacionadas à autenticação
e gerenciamento de usuários, incluindo login, logout, criação
de conta e página inicial.
"""
from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def login_view(request):
    # GET → renderiza pages/index.html (form de login)
    if request.method == "GET":
        return render(request, "pages/index.html")


def create_account(request):
    """
    View para criação de nova conta de usuário.

    Gerencia o processo de cadastro de novos usuários:
    - GET: Exibe o formulário de cadastro
    - POST: Valida e cria a conta, ou exibe erros

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Formulário de cadastro ou redirecionamento
    """
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(
            request,
            "pages/create-account.html",
            {"form": form}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Conta criada com sucesso! Faça login."
            )
            return redirect("/")

        messages.error(
            request,
            "Corrija os erros abaixo."
        )
        return render(
            request,
            "pages/create-account.html",
            {"form": form}
        )
