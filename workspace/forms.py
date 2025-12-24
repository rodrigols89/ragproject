"""
Formulários do app workspace.

Este módulo contém os formulários Django para criação e edição
de pastas e arquivos, incluindo validações customizadas.
"""
from django import forms
from django.core.exceptions import ValidationError

from .models import File, Folder


def validate_file_size(value):
    """
    Valida o tamanho máximo do arquivo.

    Args:
        value: Arquivo enviado pelo usuário

    Raises:
        ValidationError: Se o arquivo exceder o limite
    """
    max_mb = 100
    max_bytes = max_mb * 1024 * 1024

    if value.size > max_bytes:
        raise ValidationError(
            f"O arquivo não pode ser maior que {max_mb} MB."
        )


class FolderForm(forms.ModelForm):
    """
    Formulário para criação de pastas.

    Valida o nome da pasta e garante que não esteja vazio.
    """

    class Meta:
        model = Folder
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full px-3 py-2 border rounded",
                    "placeholder": "Nome da pasta",
                }
            ),
        }
        error_messages = {
            "name": {
                "required": "O nome da pasta é obrigatório."
            },
        }

    def clean_name(self):
        """
        Valida e limpa o nome da pasta.

        Remove espaços em branco e garante que não esteja vazio.

        Returns:
            str: Nome da pasta validado e limpo

        Raises:
            ValidationError: Se o nome for inválido
        """
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise ValidationError("Nome inválido.")

        return name


class FileForm(forms.ModelForm):
    """
    Formulário para upload de arquivos.

    Valida tamanho do arquivo e preenche nome automaticamente
    se não fornecido pelo usuário.
    """

    class Meta:
        model = File
        fields = ["name", "file"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full px-3 py-2 border rounded",
                    "placeholder": "Nome do arquivo (opcional)",
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={"class": "block w-full"}
            ),
        }
        error_messages = {
            "file": {
                "required": "Selecione um arquivo para enviar."
            },
        }

    file = forms.FileField(validators=[validate_file_size])

    def clean_name(self):
        """
        Valida e preenche o nome do arquivo.

        Se o usuário não informou o nome, usa o nome do arquivo
        enviado (sem o caminho completo).

        Returns:
            str: Nome do arquivo validado
        """
        name = self.cleaned_data.get("name")
        uploaded = self.cleaned_data.get("file")

        if not name and uploaded:
            return uploaded.name

        return name


class FileUploadForm(forms.ModelForm):
    """
    Formulário simplificado apenas para upload de arquivo.

    Usado quando não é necessário especificar o nome do arquivo
    separadamente.
    """

    class Meta:
        model = File
        fields = ["file"]
