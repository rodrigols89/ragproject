"""
Script de gerenciamento do Django.

Este arquivo é o ponto de entrada para comandos administrativos do Django.
Permite executar comandos como runserver, migrate, createsuperuser, etc.

Uso:
    python manage.py <comando>

Exemplos:
    python manage.py runserver
    python manage.py migrate
    python manage.py createsuperuser
"""
import os
import sys

from django.core.management import execute_from_command_line


def main():
    """
    Função principal que executa comandos administrativos do Django.

    Configura o módulo de settings e executa o comando solicitado
    através da linha de comando.
    """
    # Define o módulo de configurações do Django
    # Necessário antes de importar qualquer código Django
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "core.settings"
    )

    try:
        # Executa o comando solicitado
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        # Trata erro de importação do Django
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == "__main__":
    main()
