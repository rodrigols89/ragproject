from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import File, Folder


@login_required(login_url="/")
def workspace_home(request):
    """
    Página principal do workspace — exibe pastas e arquivos do usuário logado.
    """
    # Busca pastas raiz (sem pai) do usuário atual
    folders = Folder.objects.filter(owner=request.user, parent__isnull=True)

    # Busca arquivos que estão na raiz (sem pasta associada)
    files = File.objects.filter(uploader=request.user, folder__isnull=True)

    context = {
        "folders": folders,
        "files": files,
    }

    return render(request, "pages/workspace_home.html", context)
