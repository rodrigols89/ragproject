from django import forms
from django.core.exceptions import ValidationError

from .models import File, Folder


# Exemplo simples de validador de tamanho (50 MB)
def validate_file_size(value):
    max_mb = 50
    if value.size > max_mb * 1024 * 1024:
        raise ValidationError(f"O arquivo não pode ser maior que {max_mb} MB.")


class FolderForm(forms.ModelForm):
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
            "name": {"required": "O nome da pasta é obrigatório."},
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        # opcional: garantir unicidade no mesmo parent/owner
        if not name:
            raise ValidationError("Nome inválido.")
        return name


class FileForm(forms.ModelForm):
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
            "file": forms.ClearableFileInput(attrs={"class": "block w-full"}),
        }
        error_messages = {
            "file": {"required": "Selecione um arquivo para enviar."},
        }

    # adiciona validação de tamanho
    file = forms.FileField(validators=[validate_file_size])

    def clean_name(self):
        name = self.cleaned_data.get("name")
        uploaded = self.cleaned_data.get("file")
        if not name and uploaded:
            # se o usuário não informou o name,
            # preenche com o filename (sem path)
            return uploaded.name
        return name


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]
