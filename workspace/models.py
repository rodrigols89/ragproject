"""
Modelos do app workspace.

Este módulo define os modelos Folder e File que representam
a estrutura hierárquica de pastas e arquivos do workspace.
"""
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# ============================================================================
# FUNÇÃO AUXILIAR PARA UPLOAD
# ============================================================================


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
    # Determina o ID do usuário (dono da pasta ou uploader)
    if instance.folder and instance.folder.owner:
        user_part = f"user_{instance.folder.owner.id}"
    else:
        user_part = f"user_{instance.uploader.id}"

    # Determina o ID da pasta ou marca como raiz
    if instance.folder:
        folder_part = f"folder_{instance.folder.id}"
    else:
        folder_part = "root"

    # Limpa o nome do arquivo por segurança básica
    # Remove qualquer caminho relativo que possa estar no filename
    safe_name = os.path.basename(filename)

    return os.path.join("workspace", user_part, folder_part, safe_name)


# ============================================================================
# MODELO FOLDER (PASTA)
# ============================================================================

class Folder(models.Model):
    """
    Representa uma pasta do workspace do usuário.

    Suporta hierarquia através de self-referencing ForeignKey (parent).
    Permite criar estruturas de pastas aninhadas indefinidamente.
    """

    # Nome da pasta
    name = models.CharField(
        _("name"),
        max_length=255
    )

    # Usuário dono da pasta
    # CASCADE: se o usuário for deletado, todas suas pastas são deletadas
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="folders",
    )

    # Pasta pai (self-referencing)
    # null=True: permite pastas na raiz (sem pai)
    # blank=True: permite criar pastas sem especificar pai
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    # Data de criação (preenchida automaticamente)
    created_at = models.DateTimeField(auto_now_add=True)

    # Soft delete: marca como deletado sem remover do banco
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Ordenação padrão: mais recentes primeiro
        ordering = ["-created_at"]
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        """Representação em string do modelo."""
        return self.name


# ============================================================================
# MODELO FILE (ARQUIVO)
# ============================================================================

class File(models.Model):
    """
    Representa um arquivo armazenado no workspace.

    Pode estar dentro de uma pasta (Folder) ou na raiz do workspace.
    """

    # Nome do arquivo (pode ser diferente do nome do arquivo físico)
    name = models.CharField(
        _("name"),
        max_length=255
    )

    # Campo de arquivo com upload customizado
    # upload_to: função que define onde o arquivo será salvo
    file = models.FileField(
        _("file"),
        upload_to=workspace_upload_to
    )

    # Pasta onde o arquivo está armazenado
    # null=True: permite arquivos na raiz (sem pasta)
    # blank=True: permite criar arquivos sem especificar pasta
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )

    # Usuário que fez o upload
    # CASCADE: se o usuário for deletado, todos seus arquivos são deletados
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    # Data de upload (preenchida automaticamente)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Soft delete: marca como deletado sem remover do banco
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Ordenação padrão: mais recentes primeiro
        ordering = ["-uploaded_at"]
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        """Representação em string do modelo."""
        return self.name
