# RAG Project

 - **Project Structure:**
   - [`core/`](#core-project)
     - [`__init__.py`](#core-init-py)
     - [`asgi.py`](#core-asgi-py)
     - [`settings.py`](#core-settings-py)
     - [`urls.py`](#core-urls-py)
     - [`wsgi.py`](#core-wsgi-py)
   - [`nginx/`](#nginx)
     - [`nginx.conf`](#nginx-conf)
   - [`.editorconfig`](#editorconfig)
   - [`.env`](#env)
   - [`.pre-commit-config.yaml`](#pre-commit-config-yaml)
   - [`pyproject.toml`](#pyproject-toml)
     - [`[tool.ruff]`](#tool-ruff)
     - [`[tool.pytest.ini_options]`](#tool-pytest-ini-options)
     - [`[tool.taskipy.tasks]`](#tool-taskipy-tasks)
<!---
[WHITESPACE RULES]
- Same topic = "10" Whitespace character.
- Different topic = "50" Whitespace character.
--->


















































<!--- ( core/ ) --->

---

<div id="core-project"></div>

## `core/`

> A pasta `core` é o *“cérebro”* do projeto.

A pasta/diretório `core` é considerada o projeto Django em si — ou seja, a parte que controla:

 - Configurações globais;
 - URLs principais;
 - Startup do servidor;
 - ASGI/WSGI (para servidores web);
 - Apps registrados;
 - Middlewares;
 - Templates globais;
 - Linguagem, Timezone;
 - Banco de Dados.
 - etc.










---

<div id="core-init-py"></div>

## `__init__.py`

> **✔ O que é?**
> Define que a pasta é um módulo Python.

Por exemplo, permite fazer:

```python
from core import settings
```

ou

```python
from core.settings import INSTALLED_APPS
```










---

<div id="core-asgi-py"></div>

## `asgi.py`

> **✔ O que é?**  
> É o equivalente ao `wsgi.py`, só que para **ASGI (servidores async)**.

 - Daphne;
 - Uvicorn;
 - Hypercorn.

Se você usa:

 - WebSockets;
 - GraphQL subscriptions;
 - Django Channels;
 - Server-Sent Events;
 - streaming async.

> **✔ Django moderno usa ASGI**

Se você usa `Uvicorn + Nginx` (como no seu Docker), ele inicia o Django assim:

```bash
uvicorn core.asgi:application
```










---

<div id="core-settings-py"></div>

## `settings.py`

> **✔ O arquivo mais importante do projeto.**

Ele contém todas as *configurações globais* do projeto, como:

 - Banco de dados;
 - Apps instalados;
 - Middlewares;
 - Templates;
 - Arquivos estáticos;
 - Configuração de e-mail;
 - Linguagem;
 - Timezone;
 - Segurança.










---

<div id="core-urls-py"></div>

## `urls.py`

> **✔ É o “roteador” principal do Django.**

Ele define por onde cada requisição deve passar, distribuindo para os URLs de cada app.

[`urls.py`](core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("", include("workspace.urls")),
]
```










---

<div id="core-wsgi-py"></div>

## `wsgi.py`

> ✔ É o ponto de entrada para servidores *web WSGI*.

Como:

 - Gunicorn;
 - uWSGI;
 - mod_wsgi (Apache);

Ou seja, quando você faz deploy tradicional, o servidor web chama o arquivo:

```bash
core/wsgi.py
```



















































<!--- ( nginx/ ) --->

---

<div id="nginx"></div>

## `nginx/`

> A pasta `nginx/` geralmente contém os arquivos de configuração que serão usados pelo serviço *Nginx*.

 - **🔹 1. Configurar o Nginx como "reverso proxy":**
   - O *Nginx* fica na frente do Django/Uvicorn, recebendo todas as requisições externas primeiro.
 - **🔹 2. Servir arquivos estáticos e de mídia:**
   - O Django não é eficiente servindo arquivos estáticos
     - O Nginx é muito mais rapido nisso.
     -  /static/...
     - /media/...
 - **🔹 3. Controlar upload máximo (client_max_body_size):**
   - **NOTE:** Esse erro vem antes do Django.
   - Ou seja: o Nginx controla o tamanho dos arquivos no nível de servidor.
 - **🔹 4. Gerenciar performance, caching, headers e segurança:**
   - Nginx pode fazer:
     - Cache de respostas;
     - Compressão gzip;
     - Limitar conexões;
     - Rate limiting (proteger contra DOS);
     - Adicionar/remover headers HTTP;
     - Forçar HTTPS;
     - Redirecionamentos.
 - **🔹 5. Balanceamento de carga:**
   -  Em sistemas maiores, o *Nginx* distribui requisições para múltiplas instâncias do Django.










---

<div id="nginx-conf"></div>

## `nginx.conf`

> Esse arquivo é **a configuração principal do servidor Nginx** da sua aplicação.

[nginx.conf](nginx/nginx.conf)
```conf
server {
    listen 80;
    server_name _;

    # 🔓 Permitir uploads (dados enviados pelo usuário) de qualquer tamanho.
    # > O Django quem vai validar isso.
    client_max_body_size 0;

    # Servir arquivos estáticos diretamente
    location /static/ {
        alias /code/staticfiles/;
        expires 30d;
        access_log off;
        autoindex on;
    }

    # Servir arquivos de mídia
    location /media/ {
        alias /code/media/;
        expires 30d;
        access_log off;
        autoindex on;
    }

    # Repassar o resto das requisições para o Django (Uvicorn)
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Agora, vamos explicar algumas partes do código acima:

```conf
server {

}
```

O bloco `server` no *Nginx* define um servidor virtual, ou seja, um conjunto de regras que respondem a um domínio ou porta específica.

Dentro dele ficam as configurações que indicam:

 - Em qual porta o servidor vai ouvir.
 - Para qual domínio ele responde.
 - Como lidar com diferentes tipos de requisição (estáticos, mídia, proxy, etc.).
 - Definição de blocos `location` específicos
 - É como se fosse um site dentro do *Nginx*.
 - **NOTE:** *Tudo dentro dele define como o Nginx responde a requisições.*

```conf
listen 80;
server_name _;
client_max_body_size 0;
```

 - `listen 80;`
   - Diz ao Nginx para escutar requisições *HTTP* na porta *80*.
   - **NOTE:** É a porta padrão para HTTP (não seguro).
 - `server_name _;`
   - Define para quais domínios esse servidor responde.
   - O `_` é um coringa, indicando *“qualquer nome de servidor”*.
   - É muito usado para servidores default.
 - `client_max_body_size 0;`
   - Define o tamanho máximo permitido para uploads.
   - `0` = ilimitado.
   - Importante quando você trabalha com upload de arquivos grandes *(PDF, imagens, vídeos, etc.)*.

```conf

```


















































<!--- ( .editorconfig ) --->

---

<div id="editorconfig"></div>

## `.editorconfig`

O arquivo [.editorconfig](.editorconfig) é usado para **padronizar o estilo de código** entre diferentes editores e IDEs (como VS Code, PyCharm, Sublime, etc.).

Ele garante que, independentemente de quem edite o código e onde, as regras de formatação — como indentação, codificação de caracteres e finais de linha — sejam consistentes em todo o projeto.

[.editorconfig](.editorconfig)
```yaml
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8

# 4 space indentation
[*.{py,html, js}]
indent_style = space
indent_size = 4

# 2 space indentation
[*.{json,y{a,}ml,cwl}]
indent_style = space
indent_size = 2
```

 - `root = true`
   - ➡️ Indica que este é o arquivo `.editorconfig` principal.
   - Ou seja, o EditorConfig não deve procurar configurações em diretórios superiores.
   - Se houvesse outro `.editorconfig` acima na hierarquia, ele seria ignorado.

```yaml
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
```

 - `[*]`
   - ➡️ Essa seção aplica-se a todos os arquivos (`*` é um curinga que significa “qualquer nome e extensão”).
   - Tudo o que vier abaixo até outra seção será aplicado globalmente.
 - `end_of_line = lf`
   - ➡️ Define o tipo de quebra de linha a ser usado:
     - lf = Line Feed (Unix/Linux/Mac)
     - crlf = Carriage Return + Line Feed (Windows)
   - 👉 Aqui, está sendo forçado o estilo Unix (LF), mesmo que alguém edite no Windows.
 - `insert_final_newline = true`
   - ➡️ Garante que haverá uma linha em branco no final do arquivo.
   - Muitos compiladores e ferramentas de versionamento esperam isso (boas práticas em Unix).
 - `charset = utf-8`
   - ➡️ Define o conjunto de caracteres padrão para todos os arquivos: *UTF-8*, o mais usado atualmente.
   - Isso evita erros de acentuação ou caracteres especiais ao abrir o arquivo em diferentes sistemas.

```yaml
# 4 space indentation
[*.{py,html, js}]
indent_style = space
indent_size = 4
```

 - `[*.{py,html, js}]`
   - ➡️ Aplica estas regras a arquivos com extensões `.py`, `.html` e `.js`.
   - O `{}` indica um grupo de extensões.
 - `indent_style = space`
   - ➡️ Usa espaços em vez de tabs para indentar o código.
 - `indent_size = 4`
   - ➡️ Define que cada nível de indentação terá 4 espaços.

```yaml
# 2 space indentation
[*.{json,y{a,}ml,cwl}]
indent_style = space
indent_size = 2
```

> **NOTE:**  
> Segue a mesma lógico do bloco anterior, porém, para arquivos com extensões `.json`, `.y{a,}ml` e `.cwl` e `indentação de 2 espaços`.


















































<!--- ( .env ) --->

---

<div id="env"></div>

## `.env`

[.env](.env)
```bash
# ==========================
# CONFIGURAÇÃO DO POSTGRES
# ==========================
POSTGRES_DB=easy_rag_db                     # Nome do banco de dados a ser criado
POSTGRES_USER=easyrag                       # Usuário do banco
POSTGRES_PASSWORD=easyragpass               # Senha do banco
POSTGRES_HOST=db                            # Nome do serviço (container) do banco no docker-compose
POSTGRES_PORT=5432                          # Porta padrão do PostgreSQL

# ==========================
# CONFIGURAÇÃO DO REDIS
# ==========================
REDIS_HOST=redis                            # Nome do serviço (container) do Redis no docker-compose
REDIS_PORT=6379                             # Porta padrão do Redis

# ==========================
# CONFIGURAÇÃO DJANGO
# ==========================
DJANGO_SECRET_KEY=djangopass                # Chave secreta do Django para criptografia e segurança
DJANGO_DEBUG=True                           # True para desenvolvimento; False para produção
DJANGO_ALLOWED_HOSTS=*                      # Hosts permitidos; * libera para qualquer host

# ==========================
# CONFIGURAÇÃO DO UVICORN
# ==========================
UVICORN_HOST=0.0.0.0                        # Escutar em todas as interfaces
UVICORN_PORT=8000                           # Porta interna do app

# ==========================
# CONFIGURAÇÃO DO CELERY
# ==========================

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0      # Onde as tasks vão ser enfileiradas (Redis service redis no compose)
CELERY_RESULT_BACKEND=redis://redis:6379/1  # Onde o resultado das tasks será guardado (usar Redis DB 1 separado é comum)

# Optional - For unit tests
CELERY_TASK_ALWAYS_EAGER=False
CELERY_TASK_EAGER_PROPAGATES=True
```



















































<!--- ( .pre-commit-config.yaml ) --->

---

<div id="pre-commit-config-yaml"></div>

## `.pre-commit-config.yaml`

> O `pre-commit` é uma ferramenta Python que executa verificações automáticas antes de cada commit no Git.

Para garantir que antes de cada commit seu projeto passe por:

 - ✅ lint (usando Ruff)
 - ✅ test (com pytest)
 - ✅ coverage

```bash
poetry add --group dev pre-commit@latest
```

[.pre-commit-config.yaml](.pre-commit-config.yaml)
```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-lint
        name: ruff check
        entry: task lint
        language: system
        types: [python]
        exclude: ^(core/settings\.py|documents/migrations|users/adapter.py)

      - id: pytest-test
        name: pytest test
        entry: task test
        language: system
        types: [python]

      - id: pytest-coverage
        name: pytest coverage
        entry: task post_test
        language: system
        types: [python]
```

```yaml
repos:
  - repo: local
```

 - `repos:`
   - Lista de repositórios que contêm os hooks (ações) que serão executados.
 - `repo: local`
   - Significa que os hooks não vêm de um repositório externo, mas estão definidos localmente no próprio projeto.
 - **➡️ Em outras palavras:**
   - Você está criando hooks personalizados, não baixando-os da internet.

```yaml
- id: ruff-lint
  name: ruff check
  entry: task lint
  language: system
  types: [python]
  exclude: ^(core/settings\.py|documents/migrations|users/adapter.py)
```

| Linha              | Significado                                                                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `- id: ruff-lint`  | Identificador único do hook (usado internamente pelo pre-commit).                                                                                                                                                      |
| `name: ruff check` | Nome amigável mostrado no terminal durante a execução.                                                                                                                                                                 |
| `entry: task lint` | **Comando que será executado.** Aqui, está chamando `task lint` — ou seja, o comando “lint” definido no arquivo `Taskfile.yml` (usando a ferramenta [Taskfile](https://taskfile.dev/), comum em automação de tarefas). |
| `language: system` | Indica que o comando usa o **sistema operacional** (não precisa de ambiente Python isolado). Ele executa o comando diretamente, como se fosse rodado no terminal.                                                      |
| `types: [python]`  | Define que o hook será aplicado apenas a arquivos **Python** (arquivos `.py`).                                                                                                                                         |

```yaml
- id: pytest-test
  name: pytest test
  entry: task test
  language: system
  types: [python]
```

| Linha               | Significado                                                         |
| ------------------- | ------------------------------------------------------------------- |
| `id: pytest-test`   | ID do hook (interno ao pre-commit).                                 |
| `name: pytest test` | Nome exibido durante a execução.                                    |
| `entry: task test`  | Executa o comando `task test` — novamente, vindo do `Taskfile.yml`. |
| `language: system`  | Roda o comando diretamente no ambiente do sistema.                  |
| `types: [python]`   | Aplica o hook somente a arquivos Python.                            |

```yaml
- id: pytest-coverage
  name: pytest coverage
  entry: task post_test
  language: system
  types: [python]
```

| Linha                   | Significado                                                                    |
| ----------------------- | ------------------------------------------------------------------------------ |
| `id: pytest-coverage`   | ID do hook.                                                                    |
| `name: pytest coverage` | Nome exibido no terminal.                                                      |
| `entry: task post_test` | Executa o comando `task post_test` — outro comando definido no `Taskfile.yml`. |
| `language: system`      | Usa o shell do sistema.                                                        |
| `types: [python]`       | Aplica-se apenas a arquivos Python.                                            |

Agora nós precisamos instalar o pre-commit:

```bash
pre-commit install
```

#### Dica extra: Se quiser rodar manualmente

```bash
pre-commit run --all-files
```

> **NOTE:**  
> É interessante ter uma checagem rápida no Taskipy.

[pyproject.toml](pyproject.toml)
```toml
[tool.taskipy.tasks]
precommit = 'pre-commit run --all-files'
```















































<!--- ( pyproject.toml ) --->

---

<div id="pyproject-toml"></div>

## `pyproject.toml`

O arquivo `pyproject.toml` é um arquivo de configuração padrão para projetos Python.
Ele centraliza informações sobre:

 - Dependências (bibliotecas necessárias para rodar o projeto);
 - Configuração de build (empacotamento e instalação);
 - Ferramentas de desenvolvimento (como Black, isort, Flake8, pytest, mypy, entre outras);
 - Metadados do projeto (nome, versão, autor, licença, etc.).

> **📦 Em resumo:**  
> O pyproject.toml é o coração da configuração moderna de um projeto Python.

#### 🏗️ Por que ele foi criado

Antes do `pyproject.toml`, cada ferramenta tinha seu próprio arquivo:

 - `setup.py` (empacotamento e distribuição);
 - `requirements.txt` (dependências);
 - `tox.ini` / `.flake8` / `pytest.ini` (configurações de ferramentas).

Isso tornava os projetos fragmentados e difíceis de manter.

> **👉 A partir do PEP 518 (e depois PEP 621)**  
> O Python passou a adotar o `TOML` como formato de configuração padrão — assim, tudo fica unificado em um só arquivo.










---

<div id="tool-ruff"></div>

## `[tool.ruff]`

```bash
poetry add --group dev ruff@latest
```

> Esse bloco define às *Regras Gerais de funcionamento do (Ruff)*.

#### `[tool.ruff]`

[pyproject.toml](pyproject.toml)
```toml
[tool.ruff]
line-length = 79
exclude = [
    "core/settings.py",
    "workspace/migrations",
    "users/adapter.py",
    "workspace/urls.py"
]
```

 - `line-length = 79`
   - Define que nenhuma linha de código deve ultrapassar 79 caracteres *(seguindo o padrão tradicional do PEP 8)*.
   - É especialmente útil para manter legibilidade em terminais com largura limitada.
   - Ruff irá avisar (e, se possível, corrigir) quando encontrar linhas mais longas.
 - `exclude = []`
   - Define quais arquivos o Ruff deve ignorar.

#### `[tool.ruff.lint]`

Esse é o sub-bloco principal de configuração de linting do Ruff, ou seja, onde você define como o Ruff deve analisar o código quanto a erros, estilo, boas práticas etc.

```toml
[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
```

 - `preview = true`
   - Ativa regras experimentais (em fase de teste, mas estáveis o suficiente).
   - Pode incluir novas verificações que ainda não fazem parte do conjunto padrão.
   - Útil se você quer estar sempre com o Ruff mais “rigoroso” e atualizado.
 - `select = ['I', 'F', 'E', 'W', 'PL', 'PT']`
   - Define quais conjuntos de regras (lints) o Ruff deve aplicar ao seu código. Cada uma dessas letras corresponde a um grupo de regras:
     - `I` ([Isort](https://pycqa.github.io/isort/)): Ordenação de imports em ordem alfabética.
     - `F` ([Pyflakes](https://github.com/PyCQA/pyflakes)): Procura por alguns erros em relação a boas práticas de código.
     - `E` ([pycodestyle](https://pycodestyle.pycqa.org/en/latest/)): Erros de estilo de código.
     - `W` ([pycodestyle](https://pycodestyle.pycqa.org/en/latest/)): Avisos sobre estilo de código.
     - `PL` ([Pylint](https://pylint.pycqa.org/en/latest/index.html)): "erros" em relação a boas práticas de código.
     - `PT` ([flake8-pytest](https://pypi.org/project/flake8-pytest-style/)): Boas práticas do Pytest.

#### `[tool.ruff.format]`

O bloco [tool.ruff.format] é usado para configurar o formatador interno do Ruff, que foi introduzido recentemente como uma alternativa ao Black — mas com a vantagem de ser muito mais rápido.

```toml
[tool.ruff.format]
preview = true
quote-style = "double"
```

 - `preview = true`
   - Ativa regras experimentais (em fase de teste, mas estáveis o suficiente).
 - `quote-style = "double"`
   - Define o estilo de aspas (duplas no nosso caso) usadas pelo formatador.











---

<div id="tool-pytest-ini-options"></div>

## `[tool.pytest.ini_options]`

```bash
poetry add --group dev pytest@latest
```

O bloco `[tool.pytest.ini_options]` no `pyproject.toml` é usado para configurar o comportamento do Pytest, da mesma forma que você faria com `pytest.ini`, `setup.cfg` ou `tox.ini`:

[pyproject.toml](pyproject.toml)
```toml
[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'
```

 - `pythonpath = "."`
   - Onde o Pytest procurar arquivos Python para executar.
   - Ou seja, a partir da `raiz (.)` do nosso projeto.
 - `addopts = '-p no:warnings'`
   - Para ter uma visualização mais limpa dos testes, caso alguma biblioteca exiba uma mensagem de warning, isso será suprimido pelo pytest.












---

<div id="tool-taskipy-tasks"></div>

## `[tool.taskipy.tasks]`

```bash
poetry add --group dev taskipy@latest
```

O bloco `[tool.taskipy.tasks]` é usado para definir *tarefas (tasks)* automáticas personalizadas no seu `pyproject.toml`, usando o pacote taskipy.

[pyproject.toml](pyproject.toml)
```toml
Em breve...
```
































---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
