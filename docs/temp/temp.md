















































































---

<div id="workspace-forms"></div>

## `Customizando os formulários FolderForm e FileForm`

Aqui vamos implementar os formulários `FolderForm` e `FileForm` do app workspace, responsáveis por coletar dados do usuário de maneira segura e validada.

[forms.py](../workspace/forms.py)
```python
from django import forms

from .models import File, Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name"]  # campo que o usuário vai preencher


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]
```










































---

<div id="views-workspace-home"></div>

## `Implementando a view workspace_home()`

Aqui implementaremos a view (ação) `workspace_home()`, que será a página principal do workspace — onde o usuário logado verá suas pastas e arquivos da raiz (ou seja, que não estão dentro de nenhuma pasta).

[views.py](../workspace/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import File, Folder


@login_required(login_url="/")
def workspace_home(request):
    folders = Folder.objects.filter(owner=request.user, parent__isnull=True)
    files = File.objects.filter(uploader=request.user, folder__isnull=True)

    context = {
        "folders": folders,
        "files": files,
    }
    return render(request, "workspace/home.html", context)
```

 - `@login_required(login_url="/")`
   - Aplica uma camada de proteção à função.
   - Se o usuário **não estiver logado**, ele é redirecionado para a página `“/”` (geralmente a tela de login).
   - Se estiver logado, pode continuar normalmente.
 - `folders = Folder.objects.filter(owner=request.user, parent__isnull=True)`
   - Busca todas as pastas pertencentes ao usuário logado *(owner=request.user)*;
   - E que não têm *pasta-pai (parent__isnull=True)*:
     - Ou seja, estão na raiz do workspace.
 - `files = File.objects.filter(uploader=request.user, folder__isnull=True)`
   - Busca todos os arquivos enviados pelo usuário logado *(uploader=request.user)*;
   - Que também não estão dentro de nenhuma pasta *(folder__isnull=True)*.
 - `context = {"folders": folders, "files": files}`
   - Cria um dicionário de contexto que será passado para o template HTML.
   - Esse dicionário permite acessar as variáveis folders e files dentro do HTML.
 - `return render(request, "workspace/home.html", context)`
   - Retorna a resposta HTTP renderizando o template `workspace/home.html`, já com as pastas e arquivos do usuário logado disponíveis para exibição.








































































