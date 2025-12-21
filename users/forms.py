"""
Formulários customizados para autenticação e criação de usuários.

Este módulo contém formulários que estendem os formulários padrão
do Django para adicionar validações customizadas e traduções em
português.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ============================================================================
# FORMULÁRIO DE CRIAÇÃO DE USUÁRIO
# ============================================================================


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário customizado para criação de usuários.

    Estende UserCreationForm do Django para adicionar:
    - Campo de email obrigatório
    - Validação de email único
    - Labels e mensagens de erro em português
    """

    class Meta:
        """
        Metadados do formulário.

        Define o modelo usado, campos exibidos, labels e mensagens
        de erro customizadas.
        """
        # Modelo de usuário padrão do Django
        model = User

        # Campos exibidos no formulário (na ordem especificada)
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

        # Labels traduzidos para português
        labels = {
            "username": "Usuário",
            "email": "Email",
            "password1": "Senha",
            "password2": "Confirmar Senha",
        }

        # Mensagens de erro customizadas em português
        error_messages = {
            "username": {
                "unique": "Já existe um usuário com este nome.",
                "required": "O campo Usuário é obrigatório.",
            },
            "password2": {
                "password_mismatch": "As senhas não correspondem.",
            },
        }

    def clean_email(self):
        """
        Valida que o email não está duplicado.

        Impede que múltiplos usuários sejam criados com o mesmo
        endereço de email, garantindo unicidade do campo email.

        Returns:
            str: Email validado e limpo

        Raises:
            forms.ValidationError: Se o email já estiver cadastrado
        """
        email = self.cleaned_data.get("email")

        # Verifica se já existe um usuário com este email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return email
