"""
Modelos do app workspace.

Este módulo define os modelos Folder e File que representam
a estrutura hierárquica de pastas e arquivos do workspace.
"""
import os
import re

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def workspace_upload_to(instance, filename):
    """
    Constrói o caminho onde o arquivo será salvo dentro de MEDIA_ROOT.

    Estrutura: workspace/<user_id>/<folder_id_or_root>/<filename>

    Args:
        instance: Instância do modelo File sendo salvo
        filename: Nome original do arquivo

    Returns:
        str: Caminho relativo onde o arquivo será armazenado
    """
    try:
        if (instance.folder and
            hasattr(instance.folder, 'owner') and
            instance.folder.owner and
            hasattr(instance.folder.owner, 'id')):
            user_part = f"user_{instance.folder.owner.id}"
        elif hasattr(instance, 'uploader') and instance.uploader:
            user_part = f"user_{instance.uploader.id}"
        else:
            user_part = "user_0"
    except (AttributeError, ValueError):
        try:
            user_part = f"user_{instance.uploader.id}"
        except (AttributeError, ValueError):
            user_part = "user_0"

    try:
        if (instance.folder and
                hasattr(instance.folder, 'id') and
                instance.folder.id):
            folder_part = f"folder_{instance.folder.id}"
        else:
            folder_part = "root"
    except (AttributeError, ValueError):
        folder_part = "root"

    safe_name = os.path.basename(filename)
    safe_name = re.sub(r'[<>:"|?*\x00-\x1f]', '_', safe_name)
    safe_name = safe_name.strip()

    if not safe_name:
        safe_name = "unnamed-file"

    return os.path.join("workspace", user_part, folder_part, safe_name)


class Folder(models.Model):
    """
    Representa uma pasta do workspace do usuário.

    Suporta hierarquia através de self-referencing ForeignKey (parent).
    Permite criar estruturas de pastas aninhadas indefinidamente.
    """

    name = models.CharField(
        _("name"),
        max_length=255
    )

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
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        """Representação em string do modelo."""
        return self.name


class File(models.Model):
    """
    Representa um arquivo armazenado no workspace.

    Pode estar dentro de uma pasta (Folder) ou na raiz do workspace.
    """

    name = models.CharField(
        _("name"),
        max_length=255
    )

    file = models.FileField(
        _("file"),
        upload_to=workspace_upload_to
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        """Representação em string do modelo."""
        return self.name
