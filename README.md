[![CI](https://github.com/rodrigols89/ragproject/actions/workflows/ci.yml/badge.svg)](https://github.com/rodrigols89/ragproject/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/rodrigols89/ragproject/graph/badge.svg?token=IJSJKHK58C)](https://codecov.io/github/rodrigols89/ragproject)

# RAG Project

 - **Project Structure:**
   - [`.github/workflows`](#github-workflows)
     - [`ci.yml`](#github-workflows-ci-yml)
   - [`core/`](#core-project)
     - [`__init__.py`](#core-init-py)
     - [`asgi.py`](#core-asgi-py)
     - [`settings.py`](#core-settings-py)
       - [`TEMPLATES = []`](#settings-templates)
       - [`DATABASES = {}`](#settings-database)
     - [`urls.py`](#core-urls-py)
     - [`wsgi.py`](#core-wsgi-py)
   - [tests/](#global-tests)
   - [`nginx/`](#nginx)
     - [`nginx.conf`](#nginx-conf)
   - [`.editorconfig`](#editorconfig)
   - [`.env`](#env)
   - [`.pre-commit-config.yaml`](#pre-commit-config-yaml)
   - [`docker-compose.dev.yml (desenvolvimento)`](#)
   - [`docker-compose.prod.yml (produção)`](#)
   - [`docker-compose.yml (base)`](#)
   - [`pyproject.toml`](#pyproject-toml)
     - [`[tool.ruff]`](#tool-ruff)
     - [`[tool.pytest.ini_options]`](#tool-pytest-ini-options)
     - [`[tool.taskipy.tasks]`](#tool-taskipy-tasks)
<!---
[WHITESPACE RULES]
- Same topic = "10" Whitespace character.
- Different topic = "50" Whitespace character.
--->


















































<!--- ( .github/workflows ) --->

---

<div id="github-workflows"></div>

## `.github/workflows`

O diretório [.github/workflows](.github/workflows) é uma pasta especial que fica dentro do seu repositório no GitHub.

> 👉 É onde você define os fluxos de automação que o GitHub deve executar automaticamente — chamados de workflows.

Esses workflows são escritos em `YAML (.yml)`, e dizem ao GitHub:

 - Quando executar algo (gatilhos/triggers como push, pull request, etc.);
 - Em qual ambiente executar (como Ubuntu, Windows, etc.);
 - O que deve ser executado (os comandos, scripts ou jobs).

Por exemplo:

```bash
your-repo/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
```

Cada arquivo `.yml` dentro de [.github/workflows](.github/workflows) representa um workflow independente.

Por exemplo:

 - `ci.yml` → Faz testes automáticos e checa o código (CI = Continuous Integration);
 - `deploy.yml` → Envia o código para o servidor (CD = Continuous Deployment).

#### `O que é um “workflow” no GitHub Actions?`

Um *workflow* é composto de:

 - **Trigger (gatilho)** → Quando ele deve rodar;
 - **Jobs (tarefas)** → O que ele faz (como rodar testes, buildar imagem, etc.);
 - **Steps (passos)** → Os comandos de cada tarefa

#### `Cobrindo os testes com codecov.io`

 - Acesse: https://app.codecov.io/gh
 - Selecione seu repositório.
 - **"Select a setup option"**:
   - Selecione -> Using GitHub Actions
 - **"Step 1: Output a Coverage report file in your CI"**
   - Selecione -> Pytest
 - ...
 - **Step 3: add token as repository secret**
   - Copie -> CODECOV_TOKEN
   - Copie -> SUA-CHAVE-SECRETA
   - **NOTE:** Você vai utilizar eles no workflow `.github/workflows/ci.yml` (ex: [env](#env)).

Ótimo, agora você já tem a chave secreta para o Codecov, vá em:

 - Seu projeto/settings;
 - secrets and variables:
   - Actions.

Continuando, agora você vai clicar em `New repository secret` e adicionar:

 - Name: `CODECOV_TOKEN`
 - Secret: `YOUR-CODECOV-TOKEN`
 - Finalmente, clicar em "Add Secret".

Por fim, vamos adicionar os badges do **Codecov** e do **Pipeline**:

 - Para obter um *Pipeline badge*, altere o link abaixo para o repositório do seu projeto:
   - `[![CI](https://github.com/rodrigols89/ragproject/actions/workflows/ci.yml/badge.svg)](https://github.com/rodrigols89/ragproject/actions/workflows/ci.yml)`
 - Para obter um *Codecov badge*:
   - Acesse [https://app.codecov.io/gh/](https://app.codecov.io/gh/)
   - Selecione o projeto que está sendo monitorado pela cobertura de testes.
   - Vá em **Settings > Badges & Graphs > Markdown** e copie o badge gerado:
    - ``

<div id="github-workflows-ci-yml"></div>

#### `ci.yml`

> Esse *workflow* automatiza tarefas que devem rodar sempre que você faz `push` ou abre um `pull request`.

No nosso caso, ele executa:

 - Instalação do Python;
 - Instalação das dependências;
 - Lint com Ruff;
 - Testes com Pytest;
 - Geração de cobertura de testes;
 - Upload da cobertura para o Codecov,

> **NOTE:**  
> Ou seja: **ele garante que seu código está saudável antes de ser aceito no repositório**.

#### Por que o nome "CI"?

> **CI = Continuous Integration (Integração Contínua)**

Significa que toda mudança no código é automaticamente:

 - Testada;
 - Analisada;
 - Validada.

Antes de ser integrada ao projeto.

[ci.yml](.github/workflows/ci.yml)
```yaml
name: Lint & Test CI

on:
  push:
    branches: [ main, develop ]
    paths-ignore:
      - "README.md"
      - "**/*.md"
      - "**/*.txt"
      - "docs/**"
  pull_request:
    branches: [ main, develop ]
    paths-ignore:
      - "README.md"
      - "**/*.md"
      - "**/*.txt"
      - "docs/**"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install dependencies for lint
        run: |
          python -m venv .venv
          source .venv/bin/activate
          python -m pip install --upgrade pip
          pip install ruff
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run Ruff (lint)
        run: |
          source .venv/bin/activate
          ruff check .

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install dependencies for tests
        run: |
          python -m venv .venv
          source .venv/bin/activate
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run tests + coverage
        run: |
          source .venv/bin/activate
          pytest --cov=. --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true
          verbose: true
```

Agora, vamos explicar algumas partes do código acima:

```yaml
name: Lint & Test CI

on:
  push:
    branches: [ main, develop ]
    paths-ignore:
      - "README.md"
      - "**/*.md"
      - "**/*.txt"
      - "docs/**"
  pull_request:
    branches: [ main, develop ]
    paths-ignore:
      - "README.md"
      - "**/*.md"
      - "**/*.txt"
      - "docs/**"
```
 - `name: Lint & Test CI` → Nome visível do workflow no GitHub Actions.
 - `on:` → Você pode pensar no comando `on`, como: "Toda vez que o repositório receber o comando *x ("push" e "pull_request" no nosso caso)*.
   - `push:` → Gatilho (trigger) do workflow.
     - `branches: [ main, develop ]` → Branches que executarão as tarefas são `main` e `develop`.
     - `paths-ignore:` → Mudanças em `README.md`, `.md`, `.txt`, e até `docs/` não ativam esse CI.
   - `pull_request:` → Gatilho (trigger) do workflow.
     - `branches: [ main, develop ]` → Branches que executarão as tarefas são `main` e `develop`.
     - `paths-ignore:` → Mudanças em `README.md`, `.md`, `.txt`, e até `docs/` não ativam esse CI.

```yaml
jobs:
  ...
```

Um workflow pode ter vários `jobs` (testar, build, deploy, lint, etc.).

Cada job:

 - Roda em um runner separado;
 - Pode ser paralelo ou sequencial;
 - Contém steps (passos);
 - **NOTE:** É como um container de tarefas.

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest

    ...

  test:
    runs-on: ubuntu-latest
```

No código acima nós temos *2 jobs*:

 - `lint` e `test`:
   - Cada um rodando em uma *runner (Ubuntu)* separada.

Agora vamos explicar os jobs separadamente (e também explicar só o necessário, sem repetir o que já foi explicado em outras partes do README):

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"

    - name: Install dependencies for lint
      run: |
        python -m venv .venv
        source .venv/bin/activate
        python -m pip install --upgrade pip
        pip install ruff
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

 - `lint` → É o nome da tarefa (job).
   - `runs-on: ubuntu-latest` → A *runner (SO)* que vai rodar essa tarefa.
   - `steps` → Uma lista de passos que vão ser executados na runner.
     - `name: Checkout`
     - `uses: actions/checkout@v4` → Diz ao GitHub que queremos usar a Action oficial para clonar o repositório.
     - `name: Set up Python`
     - `uses: actions/setup-python@v4` → Action oficial que instala Python.
       - `with:` → Parâmetros da action.
         - `python-version: "3.12"` → Diz qual versão instalar.
     - `name: Install dependencies`
     - `run: |` → Vai executar comandos de shell, e o `|` permite escrever múltiplas linhas de comandos.
       - `python -m venv .venv` → Cria um ambiente virtual.
       - `source .venv/bin/activate` → Ativa o ambiente virtual.
       - `python -m pip install --upgrade pip` → Atualiza o pip.
       - `pip install ruff pytest pytest-cov` → Instala ferramentas utilizadas no CI.
       - `if [ -f requirements.txt ]; then pip install -r requirements.txt; fi`
         - Instala dependências do seu projeto somente se o arquivo existir.
     - `name: Run Ruff (lint)`
       - `run: |` → Vai executar comandos de shell, e o `|` permite escrever múltiplas linhas de comandos.
         - `source .venv/bin/activate` → Ativa o venv.
         - `ruff check .` → Roda o Ruff em todo o repositório.

> **O comando `name:` pode ser qualquer texto.**  
> Ele serve apenas como identificador visual no *GitHub Actions*, para você conseguir ler no painel.

```yaml
test:
  runs-on: ubuntu-latest
  needs: lint
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"

    - name: Install dependencies for tests
      run: |
        python -m venv .venv
        source .venv/bin/activate
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Run tests + coverage
      run: |
        source .venv/bin/activate
        pytest --cov=. --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        fail_ci_if_error: true
        verbose: true
```

 - `needs: lint` → Diz que essa tarefa depende (só vai ser executada depois) da tarefa `lint`.
 - `name: Upload coverage to Codecov`
 - `uses: codecov/codecov-action@v4` → Usa a Action oficial do Codecov.
   - `with:`
     - `token: ${{ secrets.CODECOV_TOKEN }}` → Token armazenado nos “Secrets” do repositório.
     - `fail_ci_if_error: true` → Se o upload falhar -> o job falha.
     - `verbose: true` → Mostra logs detalhados.



















































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

<div id="settings-templates"></div>

#### `TEMPLATES = []`

> O dicionário `TEMPLATES = []` diz ao Django onde ele deve procurar os templates.

[core/settings.py](core/settings.py)
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

<div id="settings-database"></div>

#### `DATABASES = {}`

Antes de começar a configurar o Django para reconhecer o PostgreSQL como Banco de Dados, vamos fazer ele reconhecer as variáveis de ambiente dentro de [core/settings.py](core/settings.py).

Primeiro, vamos instalar o `python-dotenv`:

```bash
poetry add python-dotenv@latest
```

**Outra biblioteca importante que vamos instalar agora é a "psycopg2-binary", que vai servir como driver para o PostgreSQL:**
```bash
poetry add psycopg2-binary@latest
```

Agora, vamos iniciar uma instância de `python-dotenv`:

[core/settings.py](core/settings.py)
```python
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```

> **Como testar que está funcionando?**

Primeiro, imagine que nós temos as seguinte variáveis de ambiente:

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
```

Agora vamos abrir um **shell interativo do Django**, ou seja, um terminal Python (REPL) com o Django já carregado, permitindo testar código com acesso total ao projeto.

É parecido com abrir um python normal, mas com estas diferenças:

| Recurso                           | Python normal | `manage.py shell` |
| --------------------------------- | ------------- | ----------------- |
| Carrega o Django automaticamente  | ❌ Não       | ✅ Sim            |
| Consegue acessar `settings.py`    | ❌           | ✅                |
| Consegue acessar models           | ❌           | ✅                |
| Consegue consultar banco de dados | ❌           | ✅                |
| Lê o `.env` (se Django carregar)  | ❌           | ✅                |
| Útil para debugar                 | Razoável      | Excelente         |

```bash
python manage.py shell
```

**OUTPUT:**
```bash
6 objects imported automatically (use -v 2 for details).
Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
```

**INPUT:**
```python
import os
```

**INPUT:**
```bash
print(os.getenv("POSTGRES_HOST"))
```

**OUTPUT:**
```bash
db
```

**INPUT:**
```bash
print(os.getenv("POSTGRES_PASSWORD"))
```

**OUTPUT:**
```bash
easyragpass
```

> **NOTE:**  
> Vejam que realmente nós estamos conseguindo acessar as variáveis de ambiente.

Continuando, agora vamos dizer ao Django qual Banco de Dados vamos utilizar.

Por exemplo:

[core/settings.py](core/settings.py)
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}
```

No exemplo acima nós temos um dicionário que informa ao Django como conectar ao banco de dados:

 - `ENGINE`
   - Qual backend/driver o Django usa — aqui, PostgreSQL.
 - `NAME`
   - Nome do banco.
 - `USER`
   - Usuário do banco.
 - `PASSWORD`
   - Senha do usuário.
 - `HOST`
   - Host/hostname do servidor de banco.
 - `PORT`
   - Porta TCP onde o Postgres escuta.

#### `O que os.getenv('VAR', 'default') faz, exatamente?`

`os.getenv` vem do módulo padrão `os` e faz o seguinte:

 - Tenta ler a variável de ambiente chamada 'VAR' (por exemplo POSTGRES_DB);
 - Se existir, retorna o valor da variável de ambiente;
 - Se não existir, retorna o valor padrão passado como segundo argumento ('default').

#### `Por que às vezes PASSAMOS um valor padrão (default) no código?`

 - *Conforto no desenvolvimento local:* evita quebrar o projeto se você esquecer de definir `.env`.
 - *Documentação inline:* dá uma ideia do nome esperado (easy_rag, 5432, etc.).
 - *Teste rápido:* você pode rodar `manage.py` localmente sem carregar variáveis.

> **NOTE:**  
> Mas atenção: os valores padrões não devem conter segredos reais (ex.: supersecret) no repositório público — isso é um risco de segurança.

#### `Por que não você não deveria colocar senhas no código?`

 - Repositórios (Git) podem vazar ou ser lidos por terceiros.
 - Código pode acabar em backups, imagens Docker, etc.
 - Difícil rotacionar/chavear senhas se espalhadas pelo repositório.

> **Regra prática:**  
> - *"NUNCA"* colocar credenciais reais em `settings.py`.
> - Use `.env` (não comitado) ou um *"secret manager"*.

<div id="settings-static-staticfiles-media"></div>

#### `/static/, /staticfiles & /media`

[core/settings.py](core/settings.py)
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```















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


















































<!--- ( tests/ ) --->

---

<div id="global-tests"></div>

## `tests/`

> A pasta `tests/` na raiz do projeto utilizada para testes gerais.

#### ✅ Quando faz sentido ter uma pasta tests/ na raiz?

A pasta `raiz/tests/` é útil quando você precisa testar coisas que não pertencem a nenhum app específico, como:

 - **🔧 1. Testes de Settings:**
   - Testar se variáveis de ambiente foram carregadas.
   - Testar se configurações obrigatórias existem.
   - Validar se `DEBUG`, `ALLOWED_HOSTS`, `DATABASES` foram definidos corretamente.
 - **🗺 2. Testes de URLs globais:**
   - Verificar se cada rota resolve para a view correta.
   - Testar middlewares globais.
   - Testar permissões gerais.
 - **📦 3. Testes de Integração:**
   - Algo que envolve múltiplos apps ao mesmo tempo.
   - Testes de APIs que atravessam vários domínios.
 - **🚀 4. Testes de inicialização do projeto:**
   - Testar se o Django sobe sem erros.
   - Testar se sinalizadores (signals) globais foram registrados.
 - **🔐 5. Testes de segurança global:**
   - CORS.
   - CSRF.
   - Rate-limiting.
   - Configurações gerais de autenticação.



















































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
        pass_filenames: false
        exclude: ^(core/settings\.py|documents/migrations|users/adapter.py|workspace/migrations|workspace/urls.py)

      - id: pytest-test
        name: pytest test
        entry: task test
        language: system
        types: [python]
        pass_filenames: false
        exclude: ^(core/settings\.py)

      - id: pytest-coverage
        name: pytest coverage
        entry: task post_test
        language: system
        types: [python]
        pass_filenames: false
        exclude: ^(core/settings\.py)
```

#### `pass_filenames: false`

Antes, de começarmos com as explicações do código acima vamos entender a linha `pass_filenames: false`.

> O `pass_filenames: false` faz com que o pre-commit execute o comando sem passar os arquivos modificados, forçando a execução global do comando — essencial para hooks como pytest.

#### `Quando você deve usar pass_filenames: false?`

 - **✔️ O comando *"não aceita nomes"* de arquivos:**
   - pytest;
   - coverage;
   - task test;
   - scripts customizados
 - **✔️ Você quer rodar a ferramenta no projeto inteiro:**
   - (ex.: lint geral, testes completos)
 - **✔️ O hook não trabalha com arquivos individuais:**
   - (ex.: gerar docs, buildar, rodar migrations)

#### `❌ Quando NÃO usar?`

Quando a ferramenta trabalha melhor recebendo somente arquivos alterados:

 - ❌ ruff por arquivo;
 - ❌ black por arquivo;
 - ❌ isort por arquivo;
 - ❌ prettier por arquivo.
 - **NOTE:** Nesses casos, deixar pass_filenames habilitado (padrão) é o ideal.

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



















































<!--- ( docker-compose.yml ) --->

---

<div id="docker-compose-dev"></div>

## `docker-compose.dev.yml (desenvolvimento)`

 - Hot reload (volumes com seu código local);
 - Debug ativo;
 - Erros mais verbosos;
 - Servir arquivos estáticos pelo Django;
 - Containers reiniciam automaticamente ao mudar código;
 - Segurança NÃO é prioridade...

#### `db`

[docker-compose.dev.yml](docker-compose.dev.yml)
```yaml
services:
  db:
    container_name: postgresql_dev
    restart: always
    env_file: .env
    ports:
      - "5432:5432"
```

 - `db`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `container_name: postgresql_dev`
   - Nome fixo do container (para facilitar comandos como docker logs postgresql).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
 - `ports: "5432:5432"`
   - Útil em desenvolvimento quando desejar acessar pelo host:
     - PgAdmin, DBeaver, debugging, etc.









---

<div id="docker-compose-prod"></div>

## `docker-compose.prod.yml (produção)`

 - Django rodando com gunicorn ou outro servidor WSGI;
 - Sem hot reload;
 - Sem volumes de código;
 - Segurança reforçada;
 - Arquivos estáticos servidos pelo Nginx;
 - Sem ferramentas de debug;
 - Configs específicas como:
   - client_max_body_size no Nginx;
   - Caches agressivos;
   - Workers paralelos no Gunicorn

#### `db`

[docker-compose.prod.yml](docker-compose.prod.yml)
```yaml
services:
  db:
    container_name: postgresql_prod
    restart: always
    env_file: .env
```

 - `db`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `container_name: postgresql_prod`
   - Nome fixo do container (para facilitar comandos como docker logs postgresql).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.










---

<div id="docker-compose"></div>

## `docker-compose.yml (base)`

 - Usado para definir serviços comuns.
 - ➡️ Não define volumes de código e nem porta externa.

[docker-compose.yml](docker-compose.yml)
```yaml
volumes:
  postgres_data:

networks:
  backend:
```

#### `volumes + networks`

Vamos começar explicando os `volumes` e `networks`:

```yaml
volumes:
  postgres_data:

networks:
  backend:
```

 - **🗂 1. O que são "volumes"?**
   - Volumes são lugares onde o Docker guarda dados de forma persistente.
   - Sem volumes, tudo que está dentro do container é apagado quando ele reinicia, o que seria terrível para um banco de dados, por exemplo: `postgres_data`
 - **🌐 2. O que são "networks"?**
   - Networks são redes internas criadas pelo Docker para que containers se comuniquem.
   - Por exemplo, `networks: backend:` cria uma rede chamada **backend**.
   - E quando você atribui a rede a algum container significa, que:
     - Este container “entra” na rede interna backend;
     - Ele pode conversar com outros containers que também estejam na mesma rede;
     - Ele pode usar o nome do container como hostname.

#### `db`

[docker-compose.yml](docker-compose.yml)
```yaml
services:
  db:
    image: postgres:15
    networks:
      - backend
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

 - `db`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: postgres:15`
   - Pega a versão 15 oficial do PostgreSQL no Docker Hub.
 - `networks: backend`
   - Atribui a rede *"backend"* ao container *"db"*.
 - `volumes:`
   - `postgres_data:` → Volume docker (Named Volume).
   - `/var/lib/postgresql/data` → Pasta interna do container onde o Postgres armazena os dados.

Agora vamos testar se está tudo bem no nosso container:

```bash
task opendb
```

Agora vamos listar as tabelas:

```bash
\dt+
```

**OUTPUT:**
```bash
                                               List of relations
 Schema |            Name            | Type  |  Owner  | Persistence | Access method |    Size    | Description
--------+----------------------------+-------+---------+-------------+---------------+------------+-------------
 public | auth_group                 | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_group_permissions     | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_permission            | table | easyrag | permanent   | heap          | 8192 bytes |
 public | auth_user                  | table | easyrag | permanent   | heap          | 16 kB      |
 public | auth_user_groups           | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_user_user_permissions | table | easyrag | permanent   | heap          | 0 bytes    |
 public | django_admin_log           | table | easyrag | permanent   | heap          | 8192 bytes |
 public | django_content_type        | table | easyrag | permanent   | heap          | 8192 bytes |
 public | django_migrations          | table | easyrag | permanent   | heap          | 16 kB      |
 public | django_session             | table | easyrag | permanent   | heap          | 16 kB      |
```

Agora, vamos listas as colunas da tabela `auth_user`:

```bash
\d auth_user
```

**OUTPUT:**
```bash
                                     Table "public.auth_user"
    Column    |           Type           | Collation | Nullable |             Default
--------------+--------------------------+-----------+----------+----------------------------------
 id           | integer                  |           | not null | generated by default as identity
 password     | character varying(128)   |           | not null |
 last_login   | timestamp with time zone |           |          |
 is_superuser | boolean                  |           | not null |
 username     | character varying(150)   |           | not null |
 first_name   | character varying(150)   |           | not null |
 last_name    | character varying(150)   |           | not null |
 email        | character varying(254)   |           | not null |
 is_staff     | boolean                  |           | not null |
 is_active    | boolean                  |           | not null |
 date_joined  | timestamp with time zone |           | not null |
Indexes:
    "auth_user_pkey" PRIMARY KEY, btree (id)
    "auth_user_username_6821ab7c_like" btree (username varchar_pattern_ops)
    "auth_user_username_key" UNIQUE CONSTRAINT, btree (username)
Referenced by:
    TABLE "auth_user_groups" CONSTRAINT "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
    TABLE "auth_user_user_permissions" CONSTRAINT "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
    TABLE "django_admin_log" CONSTRAINT "django_admin_log_user_id_c564eba6_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
```

Por fim, vamos listar todos os usuários (com suas colunas) já cadastrados no Banco de Dados:

```bash
select * from auth_user;
```

**OUTPUT:**
```bash
 id |                                         password                                          |          last_login           | is_superuser | username | first_name | last_name |           email            | is_staff | is_active |          date_joined
----+-------------------------------------------------------------------------------------------+-------------------------------+--------------+----------+------------+-----------+----------------------------+----------+-----------+-------------------------------
  2 | pbkdf2_sha256$1000000$Q77ZUEe8nNZFT3DLvOBMRf$pLgNiCmXRUEaX0XGmC+JX8jTrNqS5I6QMVuutC3ypTw= |                               | f            | rodrigo  |            |           | rodrigo.praxedes@gmail.com | f        | t         | 2025-10-21 10:30:23.466991+00
  3 | pbkdf2_sha256$1000000$93BBiOAKodPLbmgJJtbfBY$HLYRqEN5oCfmZKsA0iGkbbG+KbITmlz26BDl2xRMGbs= | 2025-11-02 09:19:36.900889+00 | f            | romario  |            |           | romario@gmail.com          | f        | t         | 2025-10-28 00:52:23.111699+00
  4 | pbkdf2_sha256$1000000$AW4kQwpGOjvxBWaCg5EMkC$+YnHIhK29DhI8PMJQyx3SIuOnCHGUJgvuuc0XNDrEKs= | 2025-11-02 09:36:10.701396+00 | f            | brenda   |            |           | brenda@gmail.com           | f        | t         | 2025-11-02 09:36:05.24123+00
  1 | pbkdf2_sha256$1000000$TwwCgqC0kp0GRli3xEyzhO$5r01g9G+sbI99a9a6cvgky5XudMjI/ADg+t5wO+1tHw= | 2025-11-02 10:07:32.909962+00 | t            | drigols  |            |           | drigols.creative@gmail.com | t        | t         | 2025-10-21 09:01:46.482399+00
(4 rows)
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

```bash
poetry add --group dev pytest-cov@latest
```

```bash
poetry add --group dev pytest-django@latest
```

O bloco `[tool.pytest.ini_options]` no `pyproject.toml` é usado para configurar o comportamento do Pytest, da mesma forma que você faria com `pytest.ini`, `setup.cfg` ou `tox.ini`:

[pyproject.toml](pyproject.toml)
```toml
[tool.pytest.ini_options]
pythonpath = "."
addopts = "-p no:warnings"
DJANGO_SETTINGS_MODULE = "core.settings"
```

 - `pythonpath = "."`
   - Onde o Pytest procurar arquivos Python para executar.
   - Ou seja, a partir da `raiz (.)` do nosso projeto.
 - `addopts = '-p no:warnings'`
   - Para ter uma visualização mais limpa dos testes, caso alguma biblioteca exiba uma mensagem de warning, isso será suprimido pelo pytest.
 - `DJANGO_SETTINGS_MODULE = "core.settings"`
   - Ela diz ao Django:
     - *“Use o arquivo core/settings.py como arquivo principal de configurações.”*
   - Assim:
     - O Django inicializa totalmente.
     - Carrega INSTALLED_APPS.
     - Carrega banco de dados.
     - Carrega middleware.
     - Carrega URLs.
     - Carrega templates.
     - Carrega auth, admin, etc.
   - **NOTE:** Sem essa linha, o Django não funciona durante os testes.

**🧠 Diferença dos outros campos**

| Configuração                 | Serve para                                                     |
| ---------------------------- | -------------------------------------------------------------- |
| `pythonpath = "."`           | Onde importar módulos (raiz do projeto)                        |
| `addopts`                    | Opções extras do pytest                                        |
| `DJANGO_SETTINGS_MODULE`     | Define qual arquivo de configurações Django será carregado     |










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
