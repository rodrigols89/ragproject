from django.contrib import admin

from .models import File, Folder

admin.site.register(Folder)
admin.site.register(File)
