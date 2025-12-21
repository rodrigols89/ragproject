"""
Configuração da aplicação workspace.

Este módulo define a configuração da aplicação Django,
incluindo metadados e configurações específicas do app.
"""
from django.apps import AppConfig


class WorkspaceConfig(AppConfig):
    """
    Configuração da aplicação workspace.

    Define o tipo de campo automático para chaves primárias
    e o nome da aplicação.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "workspace"
