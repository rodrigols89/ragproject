"""
Configuração da aplicação 'users'.

Este módulo define a configuração da aplicação Django 'users',
incluindo o tipo de campo automático usado para chaves primárias
nos modelos desta aplicação.
"""
from django.apps import AppConfig

# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================================


class UsersConfig(AppConfig):
    """
    Configuração da aplicação de usuários.

    Define configurações específicas da aplicação, como o tipo
    de campo automático usado para chaves primárias nos modelos.
    """

    # Tipo de campo automático para chaves primárias
    # BigAutoField suporta números maiores que AutoField
    default_auto_field = "django.db.models.BigAutoField"

    # Nome da aplicação
    name = "users"
