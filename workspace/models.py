import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def workspace_upload_to(instance, filename):
    """
    Constrói o path onde o arquivo será salvo dentro de MEDIA_ROOT:
    workspace/<user_id>/<folder_id_or_root>/<filename>
    """
    user_part = (
        f"user_{instance.folder.owner.id}"
        if instance.folder and instance.folder.owner
        else f"user_{instance.uploader.id}"
    )

    folder_part = f"folder_{instance.folder.id}" if instance.folder else "root"

    # Limpa o nome do arquivo por segurança básica
    safe_name = os.path.basename(filename)

    return os.path.join("workspace", user_part, folder_part, safe_name)


class Folder(models.Model):
    """
    Representa uma pasta do usuário. Suporta hierarquia via parent (self-FK).
    """

    name = models.CharField(_("name"), max_length=255)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="folders",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.name


class File(models.Model):
    """
    Representa um arquivo armazenado em uma pasta (Folder) ou na raiz.
    """

    name = models.CharField(_("name"), max_length=255)

    file = models.FileField(_("file"), upload_to=workspace_upload_to)

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,  # Agora aceita arquivos sem pasta
        blank=True,  # Também permite que o formulário aceite sem pasta
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        return self.name
