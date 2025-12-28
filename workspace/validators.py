"""
Validadores de arquivos do app workspace.

Este módulo contém funções de validação para arquivos enviados,
incluindo verificação de tipo (extensão) e tamanho.
"""
import os

from django.core.exceptions import ValidationError

MAX_FILE_MB = 100
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".xlsm",
    ".csv"
}

ALLOWED_FORMATTED = ", ".join(
    ext.upper() for ext in ALLOWED_EXTENSIONS
)


def validate_file_type(uploaded_file):
    """
    Valida o tipo de arquivo pela extensão.

    Verifica se a extensão do arquivo está na lista de extensões
    permitidas.

    Args:
        uploaded_file: Arquivo enviado pelo usuário

    Raises:
        ValidationError: Se a extensão não for permitida
    """
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        msg = (
            f"Arquivo inválido: '{uploaded_file.name}'. "
            f"O formato '{ext}' não é permitido. "
            f"Apenas {ALLOWED_FORMATTED} são aceitos."
        )
        raise ValidationError(msg)


def validate_file_size(uploaded_file):
    """
    Valida o tamanho do arquivo.

    Verifica se o arquivo não excede o tamanho máximo permitido.

    Args:
        uploaded_file: Arquivo enviado pelo usuário

    Raises:
        ValidationError: Se o arquivo exceder o limite
    """
    if uploaded_file.size > MAX_FILE_BYTES:
        msg = (
            f"O arquivo '{uploaded_file.name}' excede o limite "
            f"de {MAX_FILE_MB}MB."
        )
        raise ValidationError(msg)


def validate_file(uploaded_file):
    """
    Validação completa do arquivo.

    Executa todas as validações necessárias: tipo e tamanho.

    Args:
        uploaded_file: Arquivo enviado pelo usuário

    Raises:
        ValidationError: Se alguma validação falhar
    """
    validate_file_type(uploaded_file)
    validate_file_size(uploaded_file)
