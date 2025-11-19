import os

from django.core.exceptions import ValidationError

MAX_FILE_MB = 100
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx"}
ALLOWED_FORMATTED = ", ".join(ext.upper() for ext in ALLOWED_EXTENSIONS)


def validate_file_type(uploaded_file):
    """Valida o tipo de arquivo pela extensão."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        # Quebra de linha para evitar E501
        msg = (
            f"Arquivo inválido: '{uploaded_file.name}'. "
            f"O formato '{ext}' não é permitido. "
            f"Apenas {ALLOWED_FORMATTED} são aceitos."
        )
        raise ValidationError(msg)


def validate_file_size(uploaded_file):
    """Valida o tamanho do arquivo."""
    if uploaded_file.size > MAX_FILE_BYTES:
        # Outra quebra de linha para evitar E501
        msg = (
            f"O arquivo '{uploaded_file.name}' excede o limite "
            f"de {MAX_FILE_MB}MB."
        )
        raise ValidationError(msg)


def validate_file(uploaded_file):
    """
    Validação completa: tipo + tamanho.
    """
    validate_file_type(uploaded_file)
    validate_file_size(uploaded_file)
