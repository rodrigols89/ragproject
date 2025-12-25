# RAG Project

> **Tutorial de como este projeto foi desenvolvido, passo a passo.**

## Conteúdo

 - [`Adicionando .editorconfig e .gitignore`](#editorconfig-gitignore)
 - [`Iniciando o projeto com "poetry init"`](#poetry-init)
 - [`Instalando e configurando o Ruff`](#ruff-settings-pyproject)
 - [`Instalando e configurando o Pytest`](#pytest-settings-pyproject)
 - [`Instalando e configurando o pre-commit`](#precommit-settings)
 - [`Criando o container com PostgreSQL (db)`](#db-container)
 - [`Criando o container com Redis (redis_cache)`](#redis-container)
 - [`Instalando/Configurando/Exportando o Django + Uvicorn`](#django-settings)
 - [`Script de inicialização do serviço web (entrypoint.sh)`](#entrypoint-sh)
 - [`Criando o Dockerfile do serviço web`](#web-dockerfiler)
 - [`Configurando o Django para reconhecer o PostgreSQL (+ .env) como Banco de Dados`](#django-postgresql-settings)
 - [`Criando o docker compose para o container web`](#web-docker-compose)
 - [`Criando o container Nginx (nginx)`](#nginx-container)
 - [`Criando App "users"`](#app-users)
 - [`Criando a landing page da aplicação (base.html + index.html)`](#landing-page)
 - [`Criando a página de cadastro (create-account.html + DB Commands)`](#create-account)
 - [`Criando a sessão de login/logout + página home.html`](#session-home)
 - [`Criando o login com Google e GitHub`](#login-google-github)
 - [`Criando o app "workspace"`](#app-workspace)
 - [`Mapeando a rota home/ com a workspace/`](#home-to-workspace)
 - [`Modelando o workspace: Pastas (Folders) e Arquivos (Files)`](#folder-file)
 - [`Customizando os formulários FolderForm e FileForm`](#workspace-forms)
 - [`Atualizando a view (ação) para exibir as pastas e arquivos`](#update-view-to-list-folders-and-files)
 - [`Criando a "Área Principal" dos templates /home.html e /workspace_home`](#main-area-home-workspace)
 - [`Adicionando novas pastas (folders) com a view create_folder()`](#adding-new-folders)
 - [`Implementando a inserção de arquivos`](#implement-insert-files)
<!---
[WHITESPACE RULES]
- "40" Whitespace character.
--->



















































---

<div id="editorconfig-gitignore"></div>

## `Adicionando .editorconfig e .gitignore`

De início vamos adicionar os arquivos `.editorconfig` e `.gitignore` na raiz do projeto:

[.editorconfig](../.editorconfig)
```conf
# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
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

[.gitignore](../.gitignore)
```conf
É muito grande não vou exibir...
```




















































---

<div id="poetry-init"></div>

## `Iniciando o projeto com "poetry init"`

Agora vamos iniciar nosso projeto com `poetry init`:

```bash
poetry init
```




















































---

<div id="ruff-settings-pyproject"></div>

## `Instalando e configurando o Ruff`

Aqui vamos instalar e configurar o **Ruff** no nosso `pyproject.toml`:

```bash
poetry add --group dev ruff@latest
```

#### `[tool.ruff]`

> Esse bloco define às *Regras Gerais de funcionamento do (Ruff)*.

[pyproject.toml](../pyproject.toml)
```toml
[tool.ruff]
line-length = 79
exclude = [
    "core/settings.py",
]
```

 - `line-length = 79`
   - Define que nenhuma linha de código deve ultrapassar 79 caracteres *(seguindo o padrão tradicional do PEP 8)*.
   - É especialmente útil para manter legibilidade em terminais com largura limitada.
   - Ruff irá avisar (e, se possível, corrigir) quando encontrar linhas mais longas.
 - `exclude = ["core/settings.py"]`
   - Define quais arquivos o Ruff deve ignorar:
     - Nesse caso, ele vai ignorar o arquivo `core/settings.py`.

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

<div id="pytest-settings-pyproject"></div>

## `Instalando e configurando o Pytest`

Agora nós vamos instalar e configurar o **Pytest** no nosso `pyproject.toml`.

```bash
poetry add --group dev pytest@latest
```

```bash
poetry add --group dev pytest-django@latest
```

```bash
poetry add --group dev pytest-cov@latest
```

#### `[tool.pytest.ini_options]`

O bloco `[tool.pytest.ini_options]` no `pyproject.toml` é usado para configurar o comportamento do Pytest, da mesma forma que você faria com `pytest.ini`, `setup.cfg` ou `tox.ini`:

[pyproject.toml](../pyproject.toml)
```toml
[tool.pytest.ini_options]
pythonpath = "."
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = '-p no:warnings'
DJANGO_SETTINGS_MODULE = "core.settings"
```




















































---

<div id="precommit-settings"></div>

## `Instalando e configurando o pre-commit`

Para garantir que antes de cada commit seu projeto passe por:

 - ✅ lint (usando Ruff)
 - ✅ test (com pytest)
 - ✅ coverage

Você deve usar o pre-commit — uma ferramenta leve e ideal para isso. Vamos configurar passo a passo:

```bash
poetry add --group dev pre-commit
```

[.pre-commit-config.yaml](../.pre-commit-config.yaml)
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
        exclude: >
          ^(
            core/settings\.py|
            documents/migrations|
            users/adapter.py|
            workspace/migrations|
            workspace/urls.py
          )

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

[pyproject.toml](../pyproject.toml)
```toml
[tool.taskipy.tasks]
precommit = 'pre-commit run --all-files'
```




















































---

<div id="db-container"></div>

## `Criando o container com PostgreSQL (db)`

> Aqui nós vamos entender e criar um container contendo o `Banco de Dados PostgreSQL`.

 - **Função:**
   - Armazenar dados persistentes da aplicação (usuários, arquivos, prompts, etc.).
 - **Quando usar:**
   - Sempre que precisar de um banco de dados relacional robusto.
 - **Vantagens:**
   - ACID (consistência e confiabilidade).
   - Suporte avançado a consultas complexas.
 - **Desvantagens:**
   - Mais pesado que bancos NoSQL para dados muito simples.

Antes de criar nosso container contendo o *PostgreSQL* vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# Nome do banco de dados a ser criado
POSTGRES_DB=rag_db

# Usuário do banco de dados
POSTGRES_USER=raguser

# Senha do banco de dados
# Use uma senha forte em produção
POSTGRES_PASSWORD=ragpass

# Nome do serviço (container) do banco no docker-compose
# Em Docker Compose: use 'db' (nome do serviço)
# Em desenvolvimento local: use 'localhost'
POSTGRES_HOST=db

# Porta padrão do PostgreSQL
POSTGRES_PORT=5432
```

 - `POSTGRES_DB` → nome do banco criado automaticamente ao subir o container.
 - `POSTGRES_USER` → usuário administrador do banco.
 - `POSTGRES_PASSWORD` → senha do usuário do banco.
 - `POSTGRES_HOST` → para o Django se conectar, usamos o nome do serviço (db), não localhost, pois ambos estão na mesma rede docker.
 - `POSTGRES_PORT` → porta padrão 5432.

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *PostgreSQL* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  db:
    image: postgres:15
    container_name: postgresql
    restart: always
    env_file: .env
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
```

 - `db`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: postgres:15`
   - Pega a versão 15 oficial do PostgreSQL no Docker Hub.
 - `container_name: postgresql`
   - Nome fixo do container (para facilitar comandos como docker logs postgresql).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
 - `volumes:`
     - `postgres_data:` → Volume docker (Named Volume).
     - `/var/lib/postgresql/data` → pasta interna do container onde o Postgres armazena os dados.
 - `ports: 5432:5432`
   - `Primeiro 5432:` → porta no host (sua máquina).
   - `Segundo 5432:` → porta dentro do container onde o Postgres está rodando.
   - **NOTE:** Isso permite que você use o psql ou qualquer ferramenta de banco de dados (DBeaver, TablePlus, etc.) diretamente do seu PC.
 - `volumes:`
   - `postgres_data:` → Volume docker (Named Volume).
 - `networks: backend`
   - Coloca o container na rede backend para comunicação interna segura.

Agora é só subir o container:

```bash
task start_compose
```

Agora, se você desejar se conectar nesse Banco de Dados via *bash* utilize o seguinte comando (As vezes é necessário esperar o container/banco de dados subir):

**Entrar no container "postgres_db" via bash:**
```bash
docker exec -it postgresql bash
```

**Entra no banco de sados a partir das variáveis de ambiente:**
```bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

> **E os volumes como eu vejo?**

```bash
docker volume ls
```

**OUTPUT:**
```bash
DRIVER    VOLUME NAME
local     ragproject_postgres_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect ragproject_postgres_data
```

**OUTPUT:**
```bash
[
    {
        "CreatedAt": "2025-08-18T10:11:49-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "a700fdfee7f177c7f6362471e765e6d38489efcbffced2de9741a321d0b88646",
            "com.docker.compose.project": "easy-rag",
            "com.docker.compose.version": "2.39.1",
            "com.docker.compose.volume": "postgres_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/easy-rag_postgres_data/_data",
        "Name": "easy-rag_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```

 - `Mountpoint`
   - O *Mountpoint* é onde os arquivos realmente ficam, mas não é recomendado mexer manualmente lá.
   - Para interagir com os dados, use o *container* ou ferramentas do próprio serviço (por exemplo, psql no Postgres).




















































---

<div id="redis-container"></div>

## `Criando o container com Redis (redis_cache)`

> Aqui nós vamos entender e criar um container contendo um `cache Redis`.

 - **Função:**
   - Armazenar dados temporários (cache, sessões, filas de tarefas).
 - **Quando usar:**
   - Quando for necessário aumentar velocidade de acesso a dados temporários ou usar filas.
 - **Vantagens:**
   - Muito rápido (em memória).
   - Perfeito para cache e tarefas assíncronas.
 - **Desvantagens:**
   - Não indicado para dados críticos (pode perder dados em caso de reinício)

Antes de criar nosso container contendo o *Redis* vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# Nome do serviço (container) do Redis no docker-compose
# Em Docker Compose: use 'redis' (nome do serviço)
# Em desenvolvimento local: use 'localhost'
REDIS_HOST=redis

# Porta padrão do Redis
REDIS_PORT=6379
```

 - `REDIS_HOST` → nome do serviço no docker-compose.
 - `REDIS_PORT` → porta padrão 6379.
 - **NOTE:** O Redis será usado como cache e possivelmente fila de tarefas (com Celery, RQ ou outro).

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *Redis* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  redis:
    image: redis:7
    container_name: redis_cache
    restart: always
    env_file: .env
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
```

 - `redis:`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: redis:7`
   - Pega a versão 7 oficial do Redis no Docker Hub.
 - `container_name: redis_cache`
   - Nome fixo do container (para facilitar comandos como docker logs redis_cache).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
 - `volumes:`
     - `redis_data:` → Volume docker (Named Volume).
     - `/data` → pasta interna do container onde o Redis armazena os dados.
 - `networks: backend`
   - Só está acessível dentro da rede interna backend (não expõe porta para fora).

Agora é só subir o container:

```bash
docker compose up -d
```

> **E os volumes como eu vejo?**

```bash
docker volume ls
```

**OUTPUT:**
```bash
DRIVER    VOLUME NAME
local     ragproject_redis_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect ragproject_redis_data
```

**OUTPUT:**
```bash
[
    {
        "CreatedAt": "2025-11-10T07:35:18-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "75e82217f9045c1c51074e1c927a0ba2be71af9e784263a59e10d6bfb25e12e6",
            "com.docker.compose.project": "ragproject",
            "com.docker.compose.version": "2.39.1",
            "com.docker.compose.volume": "redis_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/ragproject_redis_data/_data",
        "Name": "ragproject_redis_data",
        "Options": null,
        "Scope": "local"
    }
]
```

 - `Mountpoint`
   - O *Mountpoint* é onde os arquivos realmente ficam, mas não é recomendado mexer manualmente lá.
   - Para interagir com os dados, use o *container* ou ferramentas do próprio serviço (por exemplo, psql no Postgres).




















































---

<div id="django-settings"></div>

## `Instalando/Configurando/Exportando o Django + Uvicorn`

 - Antes de criar um container contendo o Django, vamos instalar e configurar o Django + Uvicorn na nossa máquina local (host).
 - **NOTE:** Vai ser como um modelo que nós vamos utilizar dentro do container.

#### `Instalações iniciais`

De início, vamos instalar as bibliotecas necessárias:

```bash
poetry add django@latest
```

```bash
poetry add uvicorn@latest
```

#### `Criando o projeto Django (core)`

Agora vamos criar o projeto (core) que vai ter as configurações iniciais do Django:

```bash
django-admin startproject core .
```

#### `Configurando os arquivos: templates, static e media`

> Aqui nós vamos fazer as configurações iniciais do Django que serão.

Fazer o Django identificar onde estarão os arquivos `templates`, `static` e `media`:

[core/settings.py](../core/settings.py)
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



STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Até aqui está quase tudo ok para criarmos um Container com `Django` e `Uvicorn`...

> Mas, antes de criar nossos containers, precisamos gerar os `requirements.txt` e `requirements-dev.txt`.

**Mas, primeiro devemos instalar o plugin "export" do Poetry:**
```bash
poetry self add poetry-plugin-export
```

Agora vamos gerar o `requirements.txt` de *produção*:

**Produção:**
```bash
task exportprod
```

Continuando, agora vamos gerar `requirements-dev.txt` (esse é mais utilizado durante o desenvolvimento para quem não usa o Poetry):

**Desenvolvimento:**
```bash
task exportdev
```

Outra coisa importante agora é excluir o arquivo `core/settings.py` do ruff:

[pyproject.toml](../pyproject.toml)
```bash
[tool.ruff]
line-length = 79
exclude = [
    "core/settings.py",
]
```

> **NOTE:**  
> Agora esse arquivo não vai mais passar pelo `lint`.




















































---

<div id="entrypoint-sh"></div>

## `Script de inicialização do serviço web (entrypoint.sh)`

> O arquivo [entrypoint.sh](../entrypoint.sh) é o script de inicialização do container Docker do projeto.

Ele é executado antes do Django subir, garantindo que o ambiente esteja corretamente preparado para rodar a aplicação com segurança.

As responsabilidades principais desse script são:

 - Criar diretórios essenciais (static, media e staticfiles);
 - Ajustar permissões e ownership desses diretórios;
 - Garantir que a aplicação não rode como root, mas sim como um usuário não privilegiado (appuser);
 - Executar o comando final do container de forma segura.

Esse padrão é altamente recomendado em ambientes Docker de produção, especialmente em projetos Django.

[entrypoint.sh](../entrypoint.sh)
```bash
#!/bin/bash
set -e

# Cria diretórios necessários se não existirem
mkdir -p /code/static /code/media /code/staticfiles

# Ajusta permissões e ownership dos diretórios
# Garante que o usuário appuser (UID 1000) possa escrever neles
chmod -R /code/static 755 /code/media /code/staticfiles

# Obtém o UID do appuser (geralmente 1000)
APPUSER_UID=$(id -u appuser 2>/dev/null || echo "1000")
APPUSER_GID=$(id -g appuser 2>/dev/null || echo "1000")

# Ajusta ownership se estiver rodando como root
if [ "$(id -u)" = "0" ]; then
    chown -R ${APPUSER_UID}:${APPUSER_GID} \
        /code/media /code/staticfiles 2>/dev/null || true
    # Executa o comando como appuser
    exec gosu appuser "$@"
else
    # Se já estiver rodando como appuser, apenas executa
    exec "$@"
fi
```

 - `#!/bin/bash`
   - Define que o script será interpretado pelo Bash.
   - Sem isso, o sistema pode tentar executar com outro shell incompatível.
 - `set -e`
   - Faz o script encerrar imediatamente se qualquer comando retornar erro (exit code ≠ 0).
   - Isso evita que o container suba parcialmente configurado.
 - `mkdir -p /code/static /code/media /code/staticfiles`
   - Cria os diretórios necessários para o Django:
     - `/code/static` → arquivos estáticos coletados;
     - `/code/media` → arquivos enviados pelos usuários;
     - `/code/staticfiles` → arquivos estáticos coletados
   - **NOTE:** A flag `-p` evita erro caso os diretórios já existam.
 - `chmod -R 755 /code/media /code/staticfiles`
   - Ajusta permissões recursivamente:
     - `Owner:` leitura, escrita e execução;
     - `Grupo:` leitura e execução;
     - `Outros:` leitura e execução.
   - **NOTE:** Isso garante acesso suficiente sem abrir permissões perigosas (777).
 - `APPUSER_UID=$(id -u appuser 2>/dev/null || echo "1000")`
   - Tenta obter o UID do usuário appuser.
   - Se o usuário existir → usa o UID real.
   - Se não existir → usa 1000 como fallback.
   - `2>/dev/null` evita poluir o log com erros.
 - `APPUSER_GID=$(id -g appuser 2>/dev/null || echo "1000")`
   - Faz o mesmo acima, porém para o GID (grupo do usuário).
 - `if [ "$(id -u)" = "0" ]; then`
   - Verifica se o script está sendo executado como root.
   - `id -u` retorna o UID do usuário atual
   - `UID 0 = root`
   - Esse é o ponto de decisão principal do script.
     - `chown -R ${APPUSER_UID}:${APPUSER_GID} \`
     - `/code/media /code/staticfiles 2>/dev/null || true`
       - Se estiver rodando como root:
         - Muda o dono dos diretórios para appuser
         - Garante que o Django possa escrever nesses caminhos
       - `||` true impede que uma falha aqui derrube o container por causa do `set -e`.
     - `exec gosu appuser "$@"`
       - Executa o comando final do container como "*appuser*", não como root.
       - Detalhes importantes:
         - `gosu` troca o usuário sem criar shell intermediário
         - `exec` substitui o processo atual
         - `$@` representa o comando do CMD ou docker-compose
       - Isso garante:
         - Segurança
         - Sinais corretos (SIGTERM, SIGINT)
         - Logs limpos
 - `else`
   - Esse bloco é executado se o container NÃO estiver rodando como root.
   - `exec "$@"`
   - Apenas executa o comando final normalmente, sem trocar de usuário.
   - Isso acontece quando:
     - O container já foi configurado para rodar como appuser
     - Ou o script foi chamado manualmente
 - `fi`
   - Finaliza a estrutura condicional.




















































---

<div id="web-dockerfiler"></div>

## `Criando o Dockerfile do serviço web`

Antes de criar o container contendo o *Django* e o *Uvicorn*, vamos criar o nosso Dockerfile...

> **Mas por que eu preciso de um Dockerfile para o Django + Uvicorn?**

**NOTE:**  
O Dockerfile é onde você diz **como** essa imagem será construída.

> **O que o Dockerfile faz nesse caso?**

 - Escolhe a imagem base (ex.: python:3.12-slim) para rodar o Python.
 - Instala as dependências do sistema (por exemplo, libpq-dev para PostgreSQL).
 - Instala as dependências Python (pip install -r requirements.txt).
 - Copia o código do projeto para dentro do container.
 - Define o diretório de trabalho (WORKDIR).
 - Configura o comando de entrada.
 - Organiza assets estáticos e outras configurações.

> **Quais as vantagens de usar o Dockerfile?**

 - **Reprodutibilidade:**
   - Qualquer pessoa consegue subir seu projeto com o mesmo ambiente que você usa.
 - **Isolamento:**
   - Evita conflitos de versão no Python e dependências.
 - **Customização:**
   - Você pode instalar pacotes de sistema ou bibliotecas específicas.
 - **Portabilidade:**
   - Mesma imagem funciona no seu PC, no servidor ou no CI/CD.

O nosso [Dockerfile](../Dockerfile) vai ficar da seguinte maneira:

[Dockerfile](../Dockerfile)
```bash
# ===============================
# 1️⃣ Imagem base
# ===============================
FROM python:3.12-slim

# ===============================
# 2️⃣ Configuração de ambiente
# ===============================
WORKDIR /code
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/code

# ===============================
# 3️⃣ Dependências do sistema
# ===============================
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    bash \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 4️⃣ Instalar dependências Python
# ===============================
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ===============================
# 5️⃣ Copiar código do projeto
# ===============================
COPY . /code/

# ===============================
# 6️⃣ Ajustes de produção
# ===============================
# Criar usuário não-root para segurança
RUN adduser --disabled-password --no-create-home appuser && \
    chown -R appuser /code

# Copia e configura o entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Define o entrypoint (roda como root para ajustar permissões)
# O entrypoint vai mudar para appuser antes de executar o comando
ENTRYPOINT ["/entrypoint.sh"]

# Mantém como root no Dockerfile - o entrypoint gerencia a mudança de usuário
# Isso permite que o entrypoint ajuste permissões antes de mudar para appuser

# ===============================
# 7️⃣ Porta exposta (Uvicorn usa 8000 por padrão)
# ===============================
EXPOSE 8000

# ===============================
# 8️⃣ Comando padrão
# ===============================
# Mantém o container rodando e abre um shell se usado com
# `docker run` sem sobrescrever comando.
CMD ["bash"]
```




















































---

<div id="django-postgresql-settings"></div>

## `Configurando o Django para reconhecer o PostgreSQL (+ .env) como Banco de Dados`

Antes de começar a configurar o Django para reconhecer o PostgreSQL como Banco de Dados, vamos fazer ele reconhecer as variáveis de ambiente dentro de [core/settings.py](../core/settings.py).

Primeiro, vamos instalar o `python-dotenv` e `psycopg2-binary`:

```bash
poetry add python-dotenv@latest
```

```bash
poetry add psycopg2-binary@latest
```

> **NOTE:**  
> Agora nós vamos ter que exportar essas bibliotecas para os nossos requirements.txt.

```bash
task exportdev
```

```bash
task exportprod
```

Agora, vamos iniciar uma instância de `python-dotenv`:

[core/settings.py](../core/settings.py)
```python
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```

> **Como testar que está funcionando?**

Primeiro, imagine que nós temos as seguinte variáveis de ambiente:

[.env](../.env)
```bash
# Nome do banco de dados a ser criado
POSTGRES_DB=rag_db

# Usuário do banco de dados
POSTGRES_USER=raguser

# Senha do banco de dados
# Use uma senha forte em produção
POSTGRES_PASSWORD=ragpass

# Nome do serviço (container) do banco no docker-compose
# Em Docker Compose: use 'db' (nome do serviço)
# Em desenvolvimento local: use 'localhost'
POSTGRES_HOST=db

# Porta padrão do PostgreSQL
POSTGRES_PORT=5432
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

6 objects imported automatically (use -v 2 for details).
Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> import os

>>> print(os.getenv("POSTGRES_HOST"))
db

>>> print(os.getenv("POSTGRES_PASSWORD"))
ragpass
```

> **NOTE:**  
> Vejam que realmente nós estamos conseguindo acessar as variáveis de ambiente.

Continuando, agora vamos dizer ao Django qual Banco de Dados vamos utilizar.

Por exemplo:

[core/settings.py](../core/settings.py)
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

Por fim, vamos testar a conexão ao banco de dados:

**Roda/Executa o comando "migrate" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py migrate
```

**OUTPUT:**
```bash
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  No migrations to apply.
```





















































---

<div id="web-docker-compose"></div>

#### `Criando o docker compose para o container web`

> Aqui vamos entender e criar um container contendo o `Django` e o `Uvicorn`.

 - **Função:**
   - Executar a aplicação Django em produção.
 - **Quando usar:**
   - Sempre para servir sua aplicação backend.
 - **Vantagens:**
   - Uvicorn é um servidor WSGI otimizado para produção.
   - Separa lógica da aplicação da entrega de arquivos estáticos.
 - **Desvantagens:**
   - Não serve arquivos estáticos eficientemente.

Antes de criar nosso container contendo o *Django* e o *Uvicorn*, vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# ============================================================================
# CONFIGURAÇÃO DO DJANGO
# ============================================================================

# Chave secreta do Django para criptografia e segurança
# Gere uma chave segura usando:
# python -c "from django.core.management.utils import \
#     get_random_secret_key; print(get_random_secret_key())"
# Em produção, use uma chave forte e única
DJANGO_SECRET_KEY=djangopass

# Modo de debug (True/False)
# True = desenvolvimento (mostra erros detalhados)
# False = produção (oculta informações sensíveis)
DJANGO_DEBUG=True

# Hosts permitidos para acessar a aplicação
# '*' = libera para qualquer host (apenas desenvolvimento)
# Em produção: seu-dominio.com,www.seu-dominio.com
# Separe múltiplos hosts por vírgula (sem espaços)
DJANGO_ALLOWED_HOSTS=*

# ============================================================================
# CONFIGURAÇÃO DO UVICORN
# ============================================================================

# Host onde o servidor irá escutar
# 0.0.0.0 = escutar em todas as interfaces (Docker)
# 127.0.0.1 = apenas localhost (desenvolvimento local)
UVICORN_HOST=0.0.0.0

# Porta interna do app Django
UVICORN_PORT=8000
```

 - `DJANGO_SECRET_KEY` → chave única e secreta usada para assinar cookies, tokens e outras partes sensíveis.
 - `DJANGO_DEBUG` → habilita/desabilita debug e mensagens de erro detalhadas.
 - `DJANGO_ALLOWED_HOSTS` → lista de domínios que o Django aceita; `*` significa todos (não recomendado para produção).
 - `UVICORN_HOST` → define o IP/host onde o servidor Uvicorn vai rodar.
 - `UVICORN_PORT` → porta interna que o container expõe para o nginx ou para acesso direto no dev.

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *web* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django
    restart: always
    env_file: .env
    environment:
      DJANGO_SETTINGS_MODULE: core.settings
    command: >
      sh -c "
      until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
        echo '⏳ Waiting for Postgres...';
        sleep 2;
      done &&
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      python manage.py runserver ${DJANGO_HOST:-0.0.0.0}:${DJANGO_PORT:-8000}
      "
    volumes:
      - .:/code
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - db
      - redis
    ports:
      - "${UVICORN_PORT}:${UVICORN_PORT}"
    networks:
      - backend

networks:
  backend:
```

> **Uma dúvida... tudo o que eu modifico no meu projeto principal é alterado no container?**

**SIM!**  
No nosso caso, sim — porque no serviço `web` você fez este mapeamento:

[docker-compose.yml](../docker-compose.yml)
```yaml
volumes:
  - .:/code
```

Isso significa que:

 - O diretório atual no seu `host (.)` é montado dentro do container em `/code`.
 - Qualquer alteração nos arquivos do seu projeto no host aparece instantaneamente no container.
 - E o inverso também vale: se você mudar algo dentro do container nessa pasta, muda no seu host.

Por fim, vamos subir o container web:

```bash
docker compose up -d
```

Se tudo ocorrer bem você pode abrir no navegador:

 - [http://localhost:8000/](http://localhost:8000/)






















































---

<div id="nginx-container"></div>

## `Criando o container Nginx (nginx)`

Para entender a necessidade do Nginx, vamos começar imaginando que nós criamos uma conta de **super usuário** no Django (pode ser na sua máquina local mesmo):

**Roda/Executa o comando "migrate" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py migrate
```

**Roda/Executa o comando "createsuperuser" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py createsuperuser
```

Agora é só abrir o **Django Admin** e verificar se temos a tabela `users`:

 - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

![img](images/nginx-01.png)  

Vejam que:

 - Está tudo mal formado;
 - Sem estilização (CSS)...

> **Por que isso?**

 - **Executando/Rodando na máquina local**:
   - Quando você roda o Django na sua máquina local (fora do container), ele serve os arquivos estáticos automaticamente porque:
     - `DEBUG=True`
     - O servidor de desenvolvimento (runserver) serve /static/ diretamente.
 - **Executando/Rodando no container**:
   - Mas dentro do Docker, o **servidor Uvicorn não serve arquivos estáticos por padrão**.
   - Uvicorn é um ASGI server puro, *não um servidor web completo (como o runserver do Django)*.
   - **NOTE:** Por isso, o Django Admin aparece sem CSS.

#### `Como resolver isso? Usando Nginx`

Para ambientes de produção profissional, você deve:

 - Deixar o Uvicorn apenas para as requisições dinâmicas (ASGI);
 - Deixar o Nginx servir /static/ e /media/ diretamente.

 - **Função:**
   - Servir arquivos estáticos e atuar como *proxy reverso* para o Django.
 - **Quando usar:**
   - Sempre em produção para segurança e desempenho.
 - **Reverse proxy:**
   - Receber as requisições HTTP/HTTPS dos clientes.
   - Redirecionar (proxy_pass) para seu container Django (web).
   - Isso permite que seu backend fique “escondido” atrás do Nginx, ganhando segurança e performance.
 - **Servir arquivos estáticos e de mídia diretamente:**
   - Em Django, arquivos estáticos (/static/) e de upload (/media/) não devem ser servidos pelo Uvicorn (ineficiente).
   - O Nginx é muito melhor para isso, então ele entrega esses arquivos direto do volume.
 - **HTTPS (SSL/TLS):**
   - Configurar certificados (ex.: Let’s Encrypt) para rodar sua aplicação com HTTPS.
   - O Django não lida com certificados nativamente, então o Nginx faz esse papel.
 - **Balanceamento e cache (futuro):**
   - Se você crescer, pode colocar vários containers de Django e usar o Nginx como load balancer.
   - Também pode configurar cache de páginas ou de assets.
 - **Vantagens:**
   - Muito rápido para servir arquivos estáticos.
   - HTTPS e balanceamento de carga.
 - **Desvantagens:**
   - Exige configuração inicial extra.
 - **👉 Resumindo:**
   - O Nginx é a porta de entrada da sua aplicação, cuidando de performance, segurança e organização.

**NOTE:**  
Mas antes de criar e iniciar o nosso container com Nginx, vamos alterar uma configuração no nosso container `web`:

[docker-compose.yml](../docker-compose.yml)
```yaml
  web:

    ...

    expose:
      - "8000"

    ...
```

> **O que mudou?**

 - **Antes nós tinhamos:**
   - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - ✅ Antes (ports) — Tornava a porta 8000 acessível externamente no host (ex.: http://localhost:8000).
 - **Agora nós temos:**
   - `expose: ["8000"]`
   - ✅ Agora (expose) — Deixa a porta 8000 visível apenas entre containers na rede Docker, invisível fora.

Com essa alteração feita, agora vamos criar/configurar o [docker-compose.yml](../docker-compose.yml) para o nosso container `nginx`:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  nginx:
    image: nginx:1.27
    container_name: nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - web
    networks:
      - backend

networks:
  backend:
```

 - `nginx:`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: nginx:1.27`
   - Pega a versão 1.27 oficial do Nginx no Docker Hub.
 - `container_name: nginx_reverse_proxy`
   - Nome fixo do container (para facilitar comandos como docker logs nginx_server).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `ports:`
   - Mapeia portas do host para o container:
     - `80:80` → HTTP
     - `443:443` → HTTPS
 - `volumes:`
   - Pasta local `./nginx/conf` → onde ficam configs do Nginx.
   - Volumes `static` e `media` para servir arquivos.
 - `depends_on:`
   - Só inicia depois que o `Django (web)` estiver rodando.
 - `networks: backend`
   - Rede interna para conversar com Django sem expor a aplicação diretamente.

Agora nós precisamos criar o arquivo de configuração do `Nginx`:

[nginx.conf](../nginx/nginx.conf)
```bash
# ============================================================================
# CONFIGURAÇÃO DO SERVIDOR WEB NGINX
# ============================================================================
#
# Este arquivo configura o Nginx como proxy reverso para a aplicação
# Django, servindo arquivos estáticos e mídia diretamente e repassando
# requisições dinâmicas para o servidor de aplicação (Uvicorn/Gunicorn).
#
# Estrutura:
# - Configurações gerais do servidor
# - Servir arquivos estáticos (CSS, JS, imagens)
# - Servir arquivos de mídia (uploads dos usuários)
# - Proxy reverso para aplicação Django
#
# ============================================================================
# CONFIGURAÇÃO DO SERVIDOR VIRTUAL
# ============================================================================

server {
    # Porta na qual o servidor escuta requisições HTTP
    listen 80;
    
    # Nome do servidor (aceita qualquer nome de domínio)
    # Em produção, substitua por um domínio específico
    server_name _;

    # ========================================================================
    # CONFIGURAÇÕES GLOBAIS DO SERVIDOR
    # ========================================================================
    
    # Tamanho máximo do corpo da requisição (0 = ilimitado)
    # Permite uploads de qualquer tamanho - a validação é feita pelo Django
    # Em produção, considere definir um limite adequado (ex: 100M)
    client_max_body_size 0;

    # ========================================================================
    # SERVIÇO DE ARQUIVOS ESTÁTICOS
    # ========================================================================
    
    # Localização para servir arquivos estáticos (CSS, JS, imagens)
    # Estes arquivos são coletados pelo Django via 'collectstatic'
    location /static/ {
        # Caminho no sistema de arquivos onde os estáticos estão
        alias /code/staticfiles/;
        
        # Cache do navegador por 30 dias
        expires 30d;
        
        # Desabilita logs de acesso para melhorar performance
        access_log off;
        
        # Habilita listagem de diretórios (útil para debug)
        autoindex on;
    }

    # ========================================================================
    # SERVIÇO DE ARQUIVOS DE MÍDIA
    # ========================================================================
    
    # Localização para servir arquivos de mídia (uploads dos usuários)
    # Estes arquivos são enviados pelos usuários e armazenados pelo Django
    location /media/ {
        # Caminho no sistema de arquivos onde os arquivos de mídia estão
        alias /code/media/;
        
        # Cache do navegador por 30 dias
        expires 30d;
        
        # Desabilita logs de acesso para melhorar performance
        access_log off;
        
        # Habilita listagem de diretórios (útil para debug)
        autoindex on;
    }

    # ========================================================================
    # PROXY REVERSO PARA APLICAÇÃO DJANGO
    # ========================================================================
    
    # Todas as outras requisições são repassadas para o servidor Django
    # O Nginx atua como proxy reverso, melhorando performance e segurança
    location / {
        # URL do servidor de aplicação (Django via Uvicorn/Gunicorn)
        # 'web' é o nome do serviço no Docker Compose
        proxy_pass http://web:8000;
        
        # Headers necessários para o Django funcionar corretamente
        # Preserva o host original da requisição
        proxy_set_header Host $host;
        
        # IP real do cliente (importante para logs e segurança)
        proxy_set_header X-Real-IP $remote_addr;
        
        # Cadeia de IPs em caso de múltiplos proxies
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Protocolo original (http ou https)
        # Necessário para o Django detectar requisições HTTPS
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Por fim, vamos subir o container `nginx`:

```bash
docker compose up -d
```

 - **🧩 Fluxo de funcionamento**
   - `Uvicorn (web)` executa o Django e responde às rotas dinâmicas.
   - `Nginx` recebe todas as requisições HTTP externas:
     - `/static/` → servido diretamente da pasta staticfiles;
     - `/media/` → servido diretamente da pasta media;
     - outras rotas → redirecionadas para o container web (Uvicorn).
   - `PostgreSQL` e Redis são usados internamente via rede backend.

Agora tente abrir:

 - [http://localhost:8000/](http://localhost:8000/)
 - [http://localhost:8000/admin/](http://localhost:8000/admin/)

> **What? Não funcionou!**  
> 👉 Porque o Nginx está na porta 80 e o Uvicorn está atrás dele, **exposto (expose)** apenas internamente no Docker.

Agora para acessar nossa aplicação `web` primeiro nós devemos passar pelo container `nginx`:

 - [http://localhost/](http://localhost/)
 - [http://localhost/admin/](http://localhost/admin/)

> **Explicando brevemente:**  
> O container *nginx* atua como `reverse proxy`; ele recebe todas as requisições HTTP (nas portas 80/443) e as encaminha internamente para o container web (Uvicorn/Django).

Agora você pode abrir o seu Django Admin que estará tudo disponível pelo Nginx:

![img](images/nginx-02.png)  

> **Mas como eu testo se meu nginx está funcionando corretamente?**

Primeiro, vamos ver se há mensagem de erro dentor do container `nginx`:

```bash
docker logs nginx
```

**OUTPUT:**
```bash
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf differs from the packaged version
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/11/10 13:10:11 [notice] 1#1: using the "epoll" event method
2025/11/10 13:10:11 [notice] 1#1: nginx/1.27.5
2025/11/10 13:10:11 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2025/11/10 13:10:11 [notice] 1#1: OS: Linux 6.6.87.2-microsoft-standard-WSL2
2025/11/10 13:10:11 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2025/11/10 13:10:11 [notice] 1#1: start worker processes
2025/11/10 13:10:11 [notice] 1#1: start worker process 28
2025/11/10 13:10:11 [notice] 1#1: start worker process 29
2025/11/10 13:10:11 [notice] 1#1: start worker process 30
2025/11/10 13:10:11 [notice] 1#1: start worker process 31
2025/11/10 13:10:11 [notice] 1#1: start worker process 32
2025/11/10 13:10:11 [notice] 1#1: start worker process 33
2025/11/10 13:10:11 [notice] 1#1: start worker process 34
2025/11/10 13:10:11 [notice] 1#1: start worker process 35
172.18.0.1 - - [10/Nov/2025:13:10:28 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:28 +0000] "GET /favicon.ico HTTP/1.1" 404 2201 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:39 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:39 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 4173 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:15:32 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:29 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:29 +0000] "GET /favicon.ico HTTP/1.1" 404 2201 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:30 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:30 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 4173 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
```

Ótimo, agora vamos fazer alguns testes no navegador:

 - http://localhost/static/ → deve(ria) exibir arquivos estáticos.
 - http://localhost/media/ → deve(ria) exibir uploads.

**OUTPUT:**
```bash
403 Forbidden
nginx/1.27.5
```

> **What? Não funcionou!**

Agora vamos tentar acessar um arquivo específico:

 - http://localhost/static/admin/css/base.css
 - http://localhost/static/admin/img/inline-delete.svg

> **What? Agora funcionou!**

 - Esse comportamento indica que o *Nginx* está conseguindo servir arquivos existentes, mas não consegue listar diretórios.
 - **NOTE:** Por padrão, o Nginx não habilita autoindex (listagem de diretórios).

Então:

 - http://localhost/static/admin/css/base.css → Funciona porque você está acessando um arquivo específico.
 - http://localhost/static/ → Dá *403 Forbidden* porque você está acessando o diretório, e o Nginx não lista o conteúdo (diretório) por padrão.

> **Como resolver isso?**

#### Habilitar autoindex (não recomendado para produção, só para teste):

[nginx.conf](../nginx/conf/nginx.conf)
```bash
location /static/ {
    alias /code/staticfiles/;
    autoindex on;
}

location /media/ {
    alias /code/media/;
    autoindex on;
}
```

**Força recriar o container `nginx`**:
```
docker compose up -d --force-recreate nginx
```

> **NOTE:**  
> Isso permite ver os arquivos listados no navegador, mas não é seguro em produção, porque expõe todos os arquivos publicamente.

Agora, abra diretamente algum arquivo, como:

 - [http://localhost/static/admin/css/base.css](http://localhost/static/admin/css/base.css)
 - [http://localhost/media/example.txt](http://localhost/media/example.txt)
   - Crie esse arquivo em `/media (host)` antes de tentar acessar (testar).

Se esses arquivos carregarem, significa que tudo está correto para servir conteúdo estático e uploads, mesmo que a listagem do diretório não funcione.

> **💡 Resumo:**  
> O erro `403` ao acessar `/static/` ou `/media/` é normal no Nginx quando você não habilita `autoindex`. Para produção, você normalmente não quer listar diretórios, apenas servir arquivos diretamente.

Outra maneira de testar se o Nginx está funcionando corretamente seria usar o `curl`:

```bash
curl http://localhost/static/admin/css/base.css -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:29:18 GMT
Content-Type: text/css
Content-Length: 22120
Last-Modified: Tue, 19 Aug 2025 01:58:34 GMT
Connection: keep-alive
ETag: "68a3da4a-5668"
Accept-Ranges: bytes
```

```bash
curl http://localhost/media/example.txt -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:30:17 GMT
Content-Type: text/plain
Content-Length: 15
Last-Modified: Tue, 19 Aug 2025 02:26:29 GMT
Connection: keep-alive
ETag: "68a3e0d5-f"
Accept-Ranges: bytes
```

```bash
curl http://localhost/static/admin/img/inline-delete.svg -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:33:07 GMT
Content-Type: image/svg+xml
Content-Length: 537
Last-Modified: Tue, 19 Aug 2025 01:58:34 GMT
Connection: keep-alive
ETag: "68a3da4a-219"
Accept-Ranges: bytes
```

 - Vejam que quem está servindo os dados é o servidor Nginx e não o Django (container web).
 - Além, disso nós também estamos vendo algumas informações interessantes sobre os arquivos:
   - tipo: `text/css`, `text/plain`, `image/svg+xml`, etc.



















































---

<div id="app-users"></div>

## `Criando App "users"`

> Aqui nós vamos criar o App `users` que vai ser responsável por armazenar os dados dos nossos usuários no Banco de Dados.

```bash
python manage.py startapp users
```

[core/settings.py](../core/settings.py)
```python
INSTALLED_APPS = [
    ...
    'users',
]
```

Para não esquecer vamos já relacionar as rotas do App `users` no nosso projeto `core/urls.py`:

[core/urls.py](../core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
]
```



















































---

<div id="landing-page"></div>

## `Criando a landing page da aplicação (base.html + index.html)`

Aqui nós vamos implementar a `landing page` da nossa aplicação, mas antes disso vamos criar o nosso `HTML base` que é responsável por aplicar configurações globais aos nossos templates:

[base.html](../templates/base.html)
```html
<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <!-- ================================================================== -->
        <!-- METADADOS E CONFIGURAÇÕES BÁSICAS                                -->
        <!-- ================================================================== -->
        
        <!-- Codificação de caracteres UTF-8 -->
        <meta charset="UTF-8">
        
        <!-- Viewport para responsividade em dispositivos móveis -->
        <meta name="viewport" 
              content="width=device-width, initial-scale=1.0">
        
        <!-- Título da página (pode ser sobrescrito por templates filhos) -->
        <title>
            {% block title %}RAG Project{% endblock title %}
        </title>
        
        <!-- ================================================================== -->
        <!-- FRAMEWORKS E BIBLIOTECAS EXTERNAS                                -->
        <!-- ================================================================== -->
        
        <!-- Tailwind CSS via CDN (versão browser) -->
        <!-- Fornece utilitários de CSS para estilização rápida -->
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4">
        </script>
        
        <!-- ================================================================== -->
        <!-- BLOCOS CUSTOMIZÁVEIS                                             -->
        <!-- ================================================================== -->
        
        <!-- Bloco para adicionar elementos no <head> (CSS, meta tags, etc) -->
        {% block head %}{% endblock head %}
    </head>
    <body class="min-h-screen bg-[#343541]">
        <!-- ================================================================== -->
        <!-- CONTEÚDO PRINCIPAL                                                -->
        <!-- ================================================================== -->
        
        <!-- Bloco principal de conteúdo da página -->
        <!-- Deve ser preenchido pelos templates filhos -->
        {% block content %}{% endblock content %}
        
        <!-- ================================================================== -->
        <!-- SCRIPTS JAVASCRIPT                                                -->
        <!-- ================================================================== -->
        
        <!-- Bloco para adicionar scripts JavaScript no final do body -->
        <!-- Colocar scripts no final melhora o tempo de carregamento -->
        {% block scripts %}{% endblock scripts %}
    </body>
</html>
```

Agora sim, vamos partir para a criação da nossa `landing page`...

> **Mas, afinal, o que é um "landing page"?**

Uma `landing page` pública geralmente contem:

 - Apresentação do produto/serviço.
 - Botões de “Entrar” e “Cadastrar”.
 - Sessões com informações sobre a empresa.
 - Depoimentos, preços, etc.

Vamos começar configurando a rota/url que vai ser nosso `/`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import login_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
]
```

 - Essa rota/url `/` vai ser tratada dentro do App `users` porque futuramente nós vamos criar condições para verificar se o usuário está logado ou não no sistema.
 - Desta maneira, é interessante que essa rota/url `/` seja tratada dentro do App `users`.

Continuando, agora vamos criar uma view (ação) para essa `landing page`:

[users/views.py](../users/views.py)
```python
from django.shortcuts import render


def login_view(request):
    if request.method == "GET":
        return render(request, "pages/index.html")
```

> **NOTE:**  
> O nome desta view (ação) é `login_view()` porque futuramente nós vamos atualizar ela para tratar logins de usuários.

Por fim, vamos criar o HTML para essa `landing page`:

[templates/icons/github.svg.html](../templates/icons/github.svg.html)
```html
<!--
    Ícone SVG do GitHub.

    Este ícone é usado nos botões de login social com GitHub.
    Utiliza SVG inline para melhor performance e customização.
    O ícone é estilizado com classes Tailwind CSS.
-->
<svg class="h-5 w-5 mr-2"
     viewBox="0 0 24 24"
     fill="currentColor"
     aria-hidden="true">
    <!-- Path do logo do GitHub (gato Octocat) -->
    <path fill-rule="evenodd" 
          d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.11.82-.26.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.333-1.754-1.333-1.754-1.09-.745.083-.73.083-.73 1.205.085 1.84 1.236 1.84 1.236 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.304.762-1.603-2.665-.303-5.467-1.333-5.467-5.93 0-1.31.468-2.38 1.235-3.22-.124-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.3 1.23a11.5 11.5 0 013.003-.404c1.02.005 2.045.138 3.003.404 2.29-1.552 3.297-1.23 3.297-1.23.653 1.653.243 2.873.12 3.176.77.84 1.234 1.91 1.234 3.22 0 4.61-2.807 5.624-5.48 5.92.43.372.823 1.102.823 2.222 0 1.604-.014 2.896-.014 3.29 0 .32.217.694.825.576C20.565 21.796 24 17.297 24 12c0-6.63-5.37-12-12-12z"/>
</svg>
```

[templates/icons/google.svg.html](../templates/icons/google.svg.html)
```html
<!--
    Ícone SVG do Google.

    Este ícone é usado nos botões de login social com Google.
    Utiliza SVG inline para melhor performance e customização.
    O ícone mantém as cores oficiais do Google (azul, verde, 
    amarelo e vermelho) e é estilizado com classes Tailwind CSS.
-->
<svg class="h-5 w-5 mr-2"
     viewBox="0 0 533.5 544.3"
     xmlns="http://www.w3.org/2000/svg"
     aria-hidden="true">
    <!-- Parte azul do logo (canto superior esquerdo) -->
    <path d="M533.5 278.4c0-18.2-1.6-36-4.7-53.2H272v100.8h147.4c-6.4 34.9-26 64.5-55.5 84.3v69.9h89.6c52.5-48.3 82-119.7 82-201.8z" 
          fill="#4285F4"/>
    <!-- Parte verde do logo (canto inferior esquerdo) -->
    <path d="M272 544.3c73.5 0 135.3-24.5 180.4-66.7l-89.6-69.9c-24.9 16.7-56.9 26.6-90.8 26.6-69.7 0-128.7-47.1-149.8-110.4H31.6v69.5C76.3 494.7 169 544.3 272 544.3z" 
          fill="#34A853"/>
    <!-- Parte amarela do logo (canto inferior direito) -->
    <path d="M122.2 327.1c-11.7-34.6-11.7-72 0-106.6V150.9H31.6c-39.6 77-39.6 168.5 0 245.5l90.6-69.3z" 
          fill="#FBBC05"/>
    <!-- Parte vermelha do logo (canto superior direito) -->
    <path d="M272 107.7c39.9 0 75.7 13.7 104 40.6l78-78C403.3 24.7 337.2 0 272 0 169 0 76.3 49.6 31.6 150.9l90.6 69.5C143.3 154.8 202.3 107.7 272 107.7z" 
          fill="#EA4335"/>
</svg>
```

[templates/pages/index.html](../templates/pages/index.html)
```html
<!--
    Template da página inicial (login).

    Esta página exibe um formulário de login com suporte a:
    - Login tradicional (username/password)
    - Login social via Google e GitHub
    - Link para criação de nova conta

    Utiliza Tailwind CSS para estilização e django-allauth
    para autenticação social.
-->
{% extends "base.html" %}

{% block content %}

    <!-- ==================================================================== -->
    <!-- CONTEÚDO PRINCIPAL - ÁREA DE LOGIN                                  -->
    <!-- ==================================================================== -->
    
    <main class="min-h-screen flex items-center justify-center py-12 
                 px-4 sm:px-6 lg:px-8">
        
        <!-- ================================================================ -->
        <!-- CARD DE LOGIN                                                  -->
        <!-- ================================================================ -->
        
        <div class="max-w-md w-full space-y-8 bg-white py-8 px-6 shadow 
                    rounded-lg">
            
            <!-- ============================================================ -->
            <!-- CABEÇALHO - LOGO E TÍTULO                                   -->
            <!-- ============================================================ -->
            
            <div class="mb-6 text-center">
                <h2 class="mt-4 text-2xl font-semibold text-gray-900">
                    RAG Project
                </h2>
                <p class="mt-1 text-sm text-gray-500">
                    Faça login para acessar seu painel
                </p>
            </div>

            <!-- ============================================================ -->
            <!-- MENSAGENS DO SISTEMA                                        -->
            <!-- ============================================================ -->
            
            <!-- Exibe mensagens de erro ou sucesso do Django -->
            {% if messages %}
                <div class="mb-4">
                    {% for message in messages %}
                        <div class="text-red-600 bg-red-100 
                                    border border-red-200 rounded-md 
                                    px-4 py-2 text-sm">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            <!-- ============================================================ -->
            <!-- FORMULÁRIO DE LOGIN TRADICIONAL                             -->
            <!-- ============================================================ -->
            
            <form method="post" action="" class="space-y-6">
                <!-- Token CSRF para proteção contra ataques -->
                {% csrf_token %}

                <!-- Campo de Username -->
                <div>
                    <label for="username" 
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Usuário
                    </label>
                    <div class="mt-1">
                        <input
                            id="username"
                            name="username"
                            type="text"
                            autocomplete="username"
                            required
                            class="appearance-none block w-full px-3 
                                   py-2 border border-gray-300 
                                   rounded-md shadow-sm 
                                   placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm">
                    </div>
                </div>

                <!-- Campo de Senha -->
                <div>
                    <label for="password" 
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Senha
                    </label>
                    <div class="mt-1">
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autocomplete="current-password"
                            required
                            class="appearance-none block w-full px-3 
                                   py-2 border border-gray-300 
                                   rounded-md shadow-sm 
                                   placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm">
                    </div>
                </div>

                <!-- Botão de Submit -->
                <div>
                    <button type="submit"
                            class="w-full flex justify-center py-2 px-4 
                                   border border-transparent 
                                   rounded-md shadow-sm 
                                   text-sm font-medium 
                                   text-white bg-blue-600 
                                   hover:bg-blue-700 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-offset-2 
                                   focus:ring-blue-500">
                        Entrar
                    </button>
                </div>
            </form>

            <!-- ============================================================ -->
            <!-- DIVISOR - SEPARADOR ENTRE LOGIN TRADICIONAL E SOCIAL        -->
            <!-- ============================================================ -->
            
            <div class="mt-6 relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-200"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="bg-white px-2 text-gray-500">
                        ou continuar com
                    </span>
                </div>
            </div>

            <!-- ============================================================ -->
            <!-- BOTÕES DE LOGIN SOCIAL                                       -->
            <!-- ============================================================ -->
            
            <!-- Grid com dois botões lado a lado (Google e GitHub) -->
            <div class="mt-6 grid grid-cols-2 gap-3">
                
                <!-- Botão de Login com Google -->
                <div>
                    <a href=""
                       class="w-full inline-flex justify-center 
                              items-center py-2 px-4 border 
                              border-gray-300 rounded-md 
                              shadow-sm bg-white hover:bg-gray-50">
                        <!-- Ícone do Google -->
                        {% include "icons/google.svg.html" %}
                        <span class="text-sm font-medium 
                                     text-gray-700">
                            Google
                        </span>
                    </a>
                </div>

                <!-- Botão de Login com GitHub -->
                <div>
                    <a href=""
                       class="w-full inline-flex justify-center 
                              items-center py-2 px-4 border 
                              border-gray-300 rounded-md 
                              shadow-sm bg-white hover:bg-gray-50">
                        <!-- Ícone do GitHub -->
                        {% include "icons/github.svg.html" %}
                        <span class="text-sm font-medium 
                                     text-gray-700">
                            GitHub
                        </span>
                    </a>
                </div>
            </div>

            <!-- ============================================================ -->
            <!-- RODAPÉ - LINK PARA CADASTRO                                 -->
            <!-- ============================================================ -->
            
            <p class="mt-6 text-center text-sm text-gray-600">
                Não tem conta?
                <a href="" 
                   class="font-medium text-blue-600 
                          hover:text-blue-700">
                    Cadastrar
                </a>
            </p>

        </div>

    </main>
{% endblock %}
```

> **NOTE:**  
> Não vou comentar sobre os *CSS/TailwindCSS* utilizados porque não é o foco desse tutorial.

Finalmente, se você abrir o projeto (site) na rota/url principal vai aparecer essa `landing page`.

 - [http://localhost/](http://localhost/)

![landing page](images/index-landing-01.png)  



















































---

<div id="create-account"></div>

## `Criando a página de cadastro (create-account.html + DB Commands)`

> Aqui nós vamos criar e configurar a nossa `página de cadastro`.

De início vamos começar configurando a rota/url `create-account`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import create_account, login_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(
        route="create-account/",
        view=create_account,
        name="create-account"
    ),
]
```

Agora, antes de criar a view (ação) que vai ser responsável por redirecionar o usuário para a página de cadastro (GET) e enviar os dados para o Banco de Dados (POST) vamos criar um formulário customizado.

Para fazer esse formulário customizado vamos criar o arquivo [users/forms.py](../users/forms.py) que nada mais é que um classe para criar um formulário genêrico para o nosso App `users` utilizando de tudo o que o Django já tem pronto:

[users/forms.py](../users/forms.py)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

        labels = {
            "username": "Usuário",
            "email": "Email",
            "password1": "Senha",
            "password2": "Confirmar Senha",
        }

        error_messages = {
            "username": {
                "unique": "Já existe um usuário com este nome.",
                "required": "O campo Usuário é obrigatório.",
            },
            "password2": {
                "password_mismatch": "As senhas não correspondem.",
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return email
```

Agora vamos criar uma view (ação) para:

 - Quando alguém clicar em "Cadastrar" na [landing page (index.html)](../templates/pages/index.html) seja redirecionado para [página de cadastro (create-account.html)](../users/templates/pages/create-account.html).
 - E quando alguém cadastrar algum usuário (corretamente), ele seja salvo no Banco de Dados e depois redirecionado para a [landing page (index.html)](../templates/pages/index.html).

[users/views.py](../users/views.py)
```python
from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def create_account(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(
            request,
            "pages/create-account.html",
            {"form": form}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Conta criada com sucesso! Faça login."
            )
            return redirect("/")

        messages.error(
            request,
            "Corrija os erros abaixo."
        )
        return render(
            request,
            "pages/create-account.html",
            {"form": form}
        )
```

> **E o formulário de cadastro?**

Bem, aqui nós vamos criar um formulário (HTML) dinâmico usando os dados enviados pelo usuário:

```python
form = CustomUserCreationForm(request.POST)
return render(request, "pages/create-account.html", {"form": form})
```

O código completo para fazer isso é o seguinte:

[users/templates/pages/create-account.html](../users/templates/pages/create-account.html)
```html
{% extends "base.html" %}

{% block title %}Criar Conta{% endblock %}

{% block content %}

    <!-- ==================================================================== -->
    <!-- CONTEÚDO PRINCIPAL - ÁREA DE CADASTRO                                -->
    <!-- ==================================================================== -->
    
    <main class="min-h-screen flex items-center justify-center py-12 
                 px-4 sm:px-6 lg:px-8">
        
        <!-- ================================================================ -->
        <!-- CARD DE CADASTRO                                                 -->
        <!-- ================================================================ -->
        
        <div class="max-w-md w-full space-y-8 bg-white py-8 px-6 shadow 
                    rounded-lg">
            
            <!-- ============================================================ -->
            <!-- CABEÇALHO - TÍTULO                                           -->
            <!-- ============================================================ -->
            
            <div class="mb-6 text-center">
                <h2 class="mt-4 text-2xl font-semibold text-gray-900">
                    Criar Conta
                </h2>
                <p class="mt-1 text-sm text-gray-500">
                    Preencha os campos abaixo para se cadastrar
                </p>
            </div>

            <!-- ============================================================ -->
            <!-- MENSAGENS DO SISTEMA                                         -->
            <!-- ============================================================ -->
            
            <!-- Exibe mensagens de erro ou sucesso do Django -->
            {% if messages %}
                <div class="mb-4">
                    {% for message in messages %}
                        <div class="text-red-600 bg-red-100 
                                    border border-red-200 rounded-md 
                                    px-4 py-2 text-sm">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            <!-- ============================================================ -->
            <!-- FORMULÁRIO DE CADASTRO                                       -->
            <!-- ============================================================ -->
            
            <form method="post" action="" class="space-y-6">
                <!-- Token CSRF para proteção contra ataques -->
                {% csrf_token %}

                <!-- Erros gerais do formulário (não relacionados a campos) -->
                {{ form.non_field_errors }}

                <!-- Campo de Username -->
                <div>
                    <label for="{{ form.username.id_for_label }}"
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Usuário
                    </label>
                    <div class="mt-1">
                        <input
                            type="text"
                            name="{{ form.username.name }}"
                            id="{{ form.username.id_for_label }}"
                            value="{{ form.username.value|default_if_none:'' }}"
                            class="appearance-none block w-full px-3 py-2 
                                   border border-gray-300 rounded-md 
                                   shadow-sm placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm"
                            required>
                    </div>
                    <!-- Exibe erros de validação do campo username -->
                    {% for error in form.username.errors %}
                        <p class="text-sm text-red-600 mt-1">
                            {{ error }}
                        </p>
                    {% endfor %}
                </div>

                <!-- Campo de Email -->
                <div>
                    <label for="{{ form.email.id_for_label }}"
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Email
                    </label>
                    <div class="mt-1">
                        <input
                            type="email"
                            name="{{ form.email.name }}"
                            id="{{ form.email.id_for_label }}"
                            value="{{ form.email.value|default_if_none:'' }}"
                            class="appearance-none block w-full px-3 py-2 
                                   border border-gray-300 rounded-md 
                                   shadow-sm placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm"
                            required>
                    </div>
                    <!-- Exibe erros de validação do campo email -->
                    {% for error in form.email.errors %}
                        <p class="text-sm text-red-600 mt-1">
                            {{ error }}
                        </p>
                    {% endfor %}
                </div>

                <!-- Campo de Senha -->
                <div>
                    <label for="{{ form.password1.id_for_label }}"
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Senha
                    </label>
                    <div class="mt-1">
                        <input
                            type="password"
                            name="{{ form.password1.name }}"
                            id="{{ form.password1.id_for_label }}"
                            class="appearance-none block w-full px-3 py-2 
                                   border border-gray-300 rounded-md 
                                   shadow-sm placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm"
                            required>
                    </div>
                    <!-- Exibe erros de validação do campo password1 -->
                    {% for error in form.password1.errors %}
                        <p class="text-sm text-red-600 mt-1">
                            {{ error }}
                        </p>
                    {% endfor %}
                </div>

                <!-- Campo de Confirmar Senha -->
                <div>
                    <label for="{{ form.password2.id_for_label }}"
                           class="block text-sm font-medium 
                                  text-gray-700">
                        Confirmar Senha
                    </label>
                    <div class="mt-1">
                        <input
                            type="password"
                            name="{{ form.password2.name }}"
                            id="{{ form.password2.id_for_label }}"
                            class="appearance-none block w-full px-3 py-2 
                                   border border-gray-300 rounded-md 
                                   shadow-sm placeholder-gray-400 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-blue-500 
                                   focus:border-blue-500 sm:text-sm"
                            required>
                    </div>
                    <!-- Exibe erros de validação do campo password2 -->
                    {% for error in form.password2.errors %}
                        <p class="text-sm text-red-600 mt-1">
                            {{ error }}
                        </p>
                    {% endfor %}
                </div>

                <!-- Botão de Submit -->
                <div>
                    <button type="submit"
                            class="w-full flex justify-center py-2 px-4 
                                   border border-transparent rounded-md 
                                   shadow-sm text-sm font-medium 
                                   text-white bg-blue-600 hover:bg-blue-700 
                                   focus:outline-none focus:ring-2 
                                   focus:ring-offset-2 
                                   focus:ring-blue-500">
                        Criar Conta
                    </button>
                </div>

            </form>

            <!-- ============================================================ -->
            <!-- DIVISOR - SEPARADOR VISUAL                                   -->
            <!-- ============================================================ -->
            
            <div class="mt-6 relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-200"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="bg-white px-2 text-gray-500">ou</span>
                </div>
            </div>

            <!-- ============================================================ -->
            <!-- RODAPÉ - LINK PARA LOGIN                                     -->
            <!-- ============================================================ -->
            
            <p class="mt-6 text-center text-sm text-gray-600">
                Já tem uma conta?
                <a href="/" 
                   class="font-medium text-blue-600 
                          hover:text-blue-700">
                    Fazer login
                </a>
            </p>

        </div>

    </main>
{% endblock %}
```

**NOTE:**  
Agora, nós precisamos referenciar que quando alguém clicar em "Cadastrar" na minha `Landing Page` (index.html) seja redirecionado para a `Página de cadastro` (create-account.html).

[index.html](../templates/pages/index.html)
```html
<p class="mt-6 text-center text-sm text-gray-600">
    Não tem conta?
    <a href="{% url 'create-account' %}" 
        class="font-medium text-blue-600 
              hover:text-blue-700">
        Cadastrar
    </a>
</p>
```

Ótimo, agora vamos visualizar o resultado:

![landing page](images/create-account-01.png)  

Agora tem um porém, se você digitar senhas que não coincidem ou tentar cadastrar um usuário que já existe você vai ter um erro, como:

 - `The two password fields didn’t match.`
 - `A user with that username already exists.`

> **NOTE:**  
> Isso acontece porque o Django, por padrão, usa mensagens de *validação internas em inglês*.

Para resolver isso abra seu arquivo [core/settings.py](../core/settings.py) e localize (ou adicione, se não existir) as seguintes variáveis:

[core/settings.py](../core/settings.py)
```python
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
```

Ótimo, agora suas mensagens de erro serão em português.

> **Por fim, como eu sei que os usuários estão sendo gravados no Banco de Dados?**

Primeiro, vamos abrir o container que tem PostgreSQL:

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



















































---

<div id="session-home"></div>

## `Criando a sessão de login/logout + página home.html`

> Aqui nós vamos criar todo mecanismo de `login` e `logout` de usuários.

De início vamos começar configurando as rotas/urls em `users/urls.py`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import create_account, home_view, login_view, logout_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(route="home/", view=home_view, name="home"),
    path(route="logout/", view=logout_view, name="logout"),
    path(
        route="create-account/",
        view=create_account,
        name="create-account"
    ),
]
```

Continuando na implementação das views (ações), vamos começar implementando a view (ação) `home_view`:

[users/views.py](../users/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/")
def home_view(request):
    return render(request, "pages/home.html")
```

**Explicação das principais partes do código:**

**🧩 1. Importações necessárias**
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
```

 - `login_required`
   - É um decorator que protege a view, garantindo que somente usuários autenticados possam acessá-la.
   - Se o usuário não estiver logado, ele é automaticamente redirecionado para a página de login (definida no parâmetro login_url).
 - `render`
   - Função do Django que combina um template HTML (`home.html`) com dados do contexto (caso existam) e retorna uma resposta HTTP para o navegador.
   - É a forma mais comum de retornar páginas renderizadas em views Django.

**🧩 2. Aplicação do decorator @login_required**
```python
# Redireciona para o login se não estiver autenticado
@login_required(login_url="/")
```

 - **O que faz?**
   - Essa linha é um decorator, ou seja, um "envoltório" que executa código antes da função `home_view`.
   - Quando alguém tenta acessar `/home/`, o Django verifica:
     - Se o usuário está autenticado, executa `home_view(request)` normalmente.
     - Se não estiver autenticado, o Django interrompe a execução e redireciona automaticamente para `login_url="/"`.
 - **Por que precisamos?**
   - Garante segurança — impede acesso não autorizado a páginas internas do sistema.
   - Evita que um usuário acesse `/home/` apenas digitando a URL no navegador.
 - **Observação:**
   - O `login_url="/"` indica que a página de login é a raiz do site (`index.html`).

Continuando na implementação das views (ações), agora vamos implementar a view (ação) `login_view`:

> **NOTE:**  
> Lembram que nós já tinhamos começado a implementar essa view antes?

[users/views.py](../users/views.py)
```python
def login_view(request):
    if request.method == "GET":
        return render(request, "pages/index.html")
```

Então, agora nós vamos refatorar e finalizar para quando o usuário clicar no botão de login (diferente de antes que apenas estavamos considerando quando a página era exibida - GET) ele seja redirecionado para a rota/url `/home/`:


[users/views.py](../users/views.py)
```python
from django.contrib.auth import login, authenticate


def login_view(request):
    # Se o usuário já estiver logado, envia direto pra home
    if request.user.is_authenticated:
        return redirect("home")

    # GET → renderiza pages/index.html (form de login)
    if request.method == "GET":
        return render(request, "pages/index.html")

    # POST → processa credenciais
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(
            request,
            "Usuário ou senha inválidos."
        )
        return render(
            request,
            "pages/index.html"
        )
```

**Explicação das principais partes do código:**

**🧩 1. Checagem se já está autenticado**
```python
if request.user.is_authenticated:
    return redirect("home")
```

 - **O que faz?**  
   - Verifica se a requisição já tem um usuário autenticado (Django fornece request.user).
 - **Por que existe:**  
   - Evita que usuários logados vejam a tela de login novamente — redireciona imediatamente para a página privada (`home`).
 - **Observação:**
   - `is_authenticated` é `True` quando a sessão contém um usuário válido (cookie de sessão presente e válido).

**🧩 2. Tratamento do GET — mostrar o formulário de login**
```python
if request.method == "GET":
    return render(request, "pages/index.html")
```

 - **O que faz?**
   - Quando a página é acessada via `GET`, renderiza o template com o formulário de login.
 - **Por que existe:**
   - Separa o `fluxo de exibição do formulário (GET)` do `fluxo de processamento (POST)`.
 - **Resultado:**
   - O navegador recebe o HTML do `index.html` contendo os campos *"username"* e *"password"*.

**🧩 3. Leitura dos dados do POST e autenticação**
```python
username = request.POST.get("username")
password = request.POST.get("password")
user = authenticate(request, username=username, password=password)
```

 - **O que faz?**
   - Pega os valores enviados pelo formulário `(request.POST)` e chama `authenticate(...)`.
   - **authenticate faz:**
     - Verifica as credenciais contra o backend de autenticação (normalmente a tabela auth_user).
     - Retorna um objeto User se as credenciais baterem, caso contrário None.
 - **Por que:**
   - Permite verificar identidade sem ainda criar sessão — apenas valida.

**🧩 4. Login bem-sucedido → criar sessão e redirecionar**
```python
if user is not None:
    login(request, user)
    return redirect("home")
```

 - **O que faz?**
   - `login(request, user)`
     - Cria a sessão do usuário (Django grava na sessão o ID do usuário e configura o cookie de sessão).
   - `redirect("home")`
     - Envia o usuário à página protegida.
     - **Por que?** Estabelecimento da sessão é o passo que efetivamente **“loga”** o usuário no site; após isso, `request.user` será o usuário autenticado em requisições seguintes.

**🧩 5. Falha na autenticação → feedback e reexibir o formulário**`
```python
else:
    messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "pages/index.html")
```

 - **O que faz?**
   - Adiciona uma mensagem de erro (usando o framework `messages`) e renderiza novamente a página de login (`index.html`).
 - **Por que:**
   - Informar o usuário que as credenciais estavam incorretas e permitir uma nova tentativa, preservando a UX.
 - **Observação de segurança:**
   - Não dá detalhe sobre qual campo falhou **(boa prática para evitar user-enumeration)**.

Por fim, o nosso usuário precisa também deslogar do sistema e para isso vamos criar a view (ação) `logout_view`:

[users/views.py](../users/views.py)
```python
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect("/")
```

**Explicação das principais partes do código:**

**🧩 1. Encerramento da sessão do usuário**
```python
logout(request)
```

 - **O que faz?**
   - Chama a função `logout()` do Django, que remove o usuário autenticado da sessão.
   - Isso significa que:
     - O cookie de autenticação é apagado.
     - `request.user` deixa de ser o usuário logado e passa a ser `AnonymousUser`.
   - A sessão no banco de dados (ou no cache, dependendo da configuração) é destruída.
 - **Por que existe?**
   - Garante que o usuário saia com segurança do sistema, protegendo o acesso à conta em dispositivos compartilhados.
 - **Importante:**
   - Essa função não precisa de parâmetros extras — o Django automaticamente identifica e limpa a sessão ativa a partir do request.

**🧩 2. Redirecionamento após logout**
```python
return redirect("/")
```

 - **O que faz?**
   - Redireciona o usuário de volta para a página de login (raiz `/`).
 - **Por que existe?**
   - Depois que o usuário sai, não faz sentido mantê-lo em uma página protegida (`home`, por exemplo);
   - Enviar de volta para `/ (login)` é o comportamento padrão e esperado após logout.
 - **Resultado final:**
   - Sessão encerrada;
   - Usuário anônimo;
   - Redirecionamento automático para a tela de login.

> **Ótimo, o que falta agora?**  

Implementar o template [users/templates/pages/home.html](../users/templates/pages/home.html) (página de boas-vindas);

[templates/partials/sidebar.html](../templates/partials/sidebar.html)
```html
<!--
    Template parcial para a sidebar de navegação.
    
    Este componente é usado em páginas autenticadas (home e workspace)
    e contém:
    - Link de navegação entre Home e Workspace
    - Link de logout
    
    Variáveis esperadas:
    - current_page: 'home' ou 'workspace' (opcional, usado para
      destacar o link ativo)
-->
<aside class="w-64 bg-gray-900 text-white flex flex-col justify-between">
    
    <!-- Link de navegação -->
    <div class="p-2 border-b border-gray-700">
        {% if current_page == 'home' %}
            <a class="flex items-center justify-between p-2 
                      hover:bg-gray-800 rounded"
               href="">
                Workspace
            </a>
        {% else %}
            <a href="{% url 'home' %}"
               class="flex items-center justify-between 
                      p-2 hover:bg-gray-800 rounded">
                Home
            </a>
        {% endif %}
    </div>

    <!-- Link de Logout -->
    <div class="p-4 border-t border-gray-700">
        <a href="{% url 'logout' %}"
           class="block text-center text-red-400 
                  hover:text-red-300">
           Sair
        </a>
    </div>

</aside>
```

[users/templates/pages/home.html](../users/templates/pages/home.html)
```html
<!--
    Template da página home (área logada).

    Esta página é exibida após o usuário fazer login e contém:
    - Sidebar com navegação e opção de logout
    - Área principal com mensagem de boas-vindas

    Requer autenticação para acessar (decorator @login_required).
-->
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <div class="flex h-screen bg-gray-100">

        <!-- ================================================================ -->
        <!-- SIDEBAR - NAVEGAÇÃO E LOGOUT                                   -->
        <!-- ================================================================ -->
        
        {% include "partials/sidebar.html" with current_page="home" %}

        <!-- ================================================================ -->
        <!-- ÁREA PRINCIPAL - CONTEÚDO DA PÁGINA HOME                        -->
        <!-- ================================================================ -->
        
        <main class="flex-1 p-8 overflow-y-auto">
            <!-- Cabeçalho com mensagem de boas-vindas -->
            <header class="bg-white shadow px-6 py-4">
                <h1 class="text-2xl font-semibold text-gray-800">
                    Bem-vindo, {{ request.user.username }}!
                </h1>
            </header>
        </main>

    </div>
{% endblock %}
```

> **Agora é só logar e ir para a página home.html?**

**NÃO!**  
Primeiro nós precisamos setar a url/link no nosso [index.html](../templates/pages/index.html) para direcionar o usuário para a página `home` e se tudo ocorrer bem, ele será redirecionado para a `home` (página de boas-vindas):

[templates/pages/index.html](../templates/pages/index.html)
```html
<!-- Form -->
<form method="post" action="" class="space-y-6">

</form>
```

> **NOTE:**  
> No nosso exemplo só faltava definir o tipo de *método* no formulário que no nosso caso era `POST`.

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
