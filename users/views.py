"""
Views da aplicação 'users'.

Este módulo contém todas as views relacionadas à autenticação
e gerenciamento de usuários, incluindo login, logout, criação
de conta e página inicial.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


@login_required(login_url="/")
def home_view(request):
    """
    View da página inicial após login.

    Exibe a página home do usuário autenticado. Requer que o
    usuário esteja logado, caso contrário redireciona para a
    página de login.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Renderiza o template home.html
    """
    return render(request, "pages/home.html")


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


def login_view(request):
    """
    View para autenticação de usuários.

    Gerencia o processo de login:
    - Se já estiver autenticado, redireciona para home
    - GET: Exibe o formulário de login
    - POST: Autentica o usuário ou exibe erro

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponse: Formulário de login ou redirecionamento
    """
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "pages/index.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(
            request,
            "Usuário ou senha inválidos."
        )
        return render(request, "pages/index.html")


def logout_view(request):
    """
    View para encerrar sessão do usuário.

    Faz logout do usuário atual e redireciona para a página
    de login.

    Args:
        request: Objeto HttpRequest do Django

    Returns:
        HttpResponseRedirect: Redireciona para a página de login
    """
    logout(request)
    return redirect("/")
