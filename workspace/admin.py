"""
Configuração do Django Admin para o app workspace.

Este módulo registra os modelos Folder e File no painel
administrativo do Django, permitindo gerenciamento via interface web.
"""
from django.contrib import admin

from .models import File, Folder

# Registra os modelos no admin do Django
admin.site.register(Folder)
admin.site.register(File)
