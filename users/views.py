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


def create_account(request):
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


@login_required(login_url="/")
def home_view(request):
    return render(request, "pages/home.html")


def login_view(request):
    # Se o usuário já estiver logado, envia direto pra home
    if request.user.is_authenticated:
        return redirect("home")

    # GET → renderiza pages/index.html (form de login)
    if request.method == "GET":
        return render(request, "pages/index.html")

    # POST → processa credenciais
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(
            request,
            "Usuário ou senha inválidos."
        )
        return render(
            request,
            "pages/index.html"
        )


def logout_view(request):
    logout(request)
    return redirect("/")
