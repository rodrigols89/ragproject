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
 - [`Instalando e preparando o django-allauth para fazer logins sociais`](#install-django-allauth)
 - [`Pegando as credenciais (chaves) do Google e GitHub`](#google-github-credentials)
 - [`Criando um super usuário e logins sociais automaticamente`](#auto-super-user-and-social-logins)
 - [`Linkando os botões de login social`](#linking-social-buttons)
 - [`Reescrevendo as mensagens do Django Allauth`](#rewriting-allauth-messages)
 - [`Criando o app "workspace"`](#app-workspace)
 - [`Mapeando a rota home/ com a workspace/`](#home-to-workspace)
 - [`Modelando o workspace: Pastas (Folders) e Arquivos (Files)`](#modeling-folder-file)
 - [`Customizando os formulários FolderForm e FileForm`](#workspace-forms)
 - [`Atualizando a view (ação) para exibir as pastas e arquivos`](#update-view-to-list-folders-and-files)
 - [`Refatorando a exibição das pastas e arquivos (Clicks, Houver, Select, Escape, Click Outside)`](#refactor-folders-and-files-v1)
 - [`Refatorando o modal para abrir selecionando o campo de digitação`](#refatoring-modal-to-select-input)
 - [`Refatorando para quando o usuário digitar um nome para uma pasta existente`](#refatoring-to-exists-folder-name)
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

<div id="install-django-allauth"></div>

## `Instalando e preparando o django-allauth para fazer logins sociais`

#### Instalando e Configurando a biblioteca django-allauth

> Aqui nós vamos instalar e configurar o `django-allauth`, que é uma biblioteca pronta para adicionar *autenticação social (OAuth)* e *funcionalidades de conta (login, logout, registro, verificação de e-mail)* ao nosso projeto Django.

Vamos começar instalando as dependências e a biblioteca `django-allauth`:

```bash
poetry add PyJWT@latest
```

```bash
poetry add cryptography@latest
```

```bash
poetry add requests@latest
```

```bash
poetry add django-allauth@latest
```

Novamente, lembre-se de importar essas bibliotecas para os nossos `requirements.txt`:

```bash
task exportdev
```

```bash
task exportprod
```

Agora nós precisamos refletir essas alterações no nosso container:

```bash
task build_compose
```

Agora vamos adicionar os *Apps* e *Middlewares* `django-allauth` necessários no `settings.py`:

[core/settings.py](../core/settings.py)
```python
INSTALLED_APPS = [
    # Apps padrão do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Obrigatório pro allauth
    "django.contrib.sites",

    # Apps principais do allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Provedores de login social
    "allauth.socialaccount.providers.google",  # 👈 habilita login com Google
    "allauth.socialaccount.providers.github",  # 👈 habilita login com GitHub

    # Seus apps
    "users",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # ✅ Novo middleware exigido pelo Django Allauth
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

 - `django.contrib.sites`
   - App do Django que permite associar configurações a um Site (domínio) — o allauth usa isso para saber qual domínio/URL usar para callbacks OAuth.
   - Você precisará criar/ajustar um Site no admin (ou via fixtures) com SITE_ID = 1 (ver mais abaixo).
 - `allauth, allauth.account, allauth.socialaccount`
   - `allauth` é o pacote principal;
   - `account` fornece funcionalidade de conta (registro, login local, confirmação de e-mail);
   - `socialaccount` é a camada que integra provedores OAuth (Google, GitHub, etc.).
 - `allauth.socialaccount.providers.google, allauth.socialaccount.providers.github`
   - Provedores prontos do allauth — carregam os adaptadores e rotas específicas para cada provedor.
   - Adicione apenas os provedores que você pretende suportar (pode ativar mais tarde).

Agora nós vamos adicionar `context_processors.request` e configurar `AUTHENTICATION_BACKENDS` (`settings.py`):

[core/settings.py](../core/settings.py)
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # <- Necessário para allauth
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# AUTHENTICATION_BACKENDS — combine o backend padrão com o do allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",            # Seu login normal
    "allauth.account.auth_backends.AuthenticationBackend",  # Login social
]
```

Outras configurações importantes no `settings.py` são as seguintes:

[core/settings.py](../core/settings.py)
```python
SITE_ID = int(os.getenv("DJANGO_SITE_ID", 1))
LOGIN_REDIRECT_URL = "/home/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
```

 - `SITE_ID = int(os.getenv("DJANGO_SITE_ID", 1))`
   - **O que é?**
     - Faz parte do framework `django.contrib.sites`
     - Identifica qual *“site”* está ativo no projeto
   - **Por que existe?**
     - O Django permite que um mesmo projeto sirva vários sites/domínios, por exemplo:
       - ID - Domínio
       - 1 - localhost
       - 2 - example.com
   - **O SITE_ID = 1 diz:**
     - *“Use o site com ID 1 da tabela django_site”*
 - `LOGIN_REDIRECT_URL = "/home/"`
   - **O que faz?**
     - URL para onde o usuário é redirecionado após login bem-sucedido.
 - `LOGOUT_REDIRECT_URL = "/"`
   - **O que faz?**
     - URL para onde o usuário vai após logout.
 - `ACCOUNT_LOGIN_METHODS = {"username"}`
   - **O que faz?**
     - Define como o usuário pode fazer login
     - `"username"` -> Login só com username.
     - `"email"` -> Login só com email.
     - `"username_email"` -> Aceita os dois.
   - **nosso caso caso:**
     - `{"username"}`
     - ➡️ O usuário só pode logar usando username.
     - ❌ Email não é aceito para login.
 - `ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]`
   - **O que faz?**
     - Define quais campos aparecem no cadastro e se são obrigatórios.
     - O `*` significa 👉 Campo obrigatório
 - `ACCOUNT_EMAIL_VERIFICATION = "optional"`
   - **O que faz?**
     - Define se o email precisa ser confirmado ou não.
     - `"mandatory"` -> Usuário **não pode logar** sem confirmar email.
     - `"optional"` -> Email pode ser confirmado depois.
     - `"none"` -> Nenhuma verificação.




















































---

<div id="google-github-credentials"></div>

## `Pegando as credenciais (chaves) do Google e GitHub`

### Como pegar as credenciais (chaves) do Google

 - **Etapas no Console do Google:**
   - Acesse https://console.cloud.google.com/
   - Faça login e crie um novo projeto (ex: Easy RAG Auth).
   - No menu lateral, vá em:
     - APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth 2.0
   - Clique no botão “Configure consent screen”
     - Clique em `Get started`
     - **Em App Information:**
       - `App name:`
         - Easy RAG
         - Esse nome aparecerá para o usuário quando ele for fazer login pelo Google.
       - `User support email:`
         - Selecione seu e-mail pessoal (ele aparece automaticamente no menu).
         - É usado pelo Google caso o usuário queira contato sobre privacidade.
       - Cli quem `next`
     - **Em Audience:**
       - Aqui o Google vai perguntar quem pode usar o aplicativo.
       - ✅ External (Externo):
         - Isso significa que qualquer usuário com uma conta Google poderá fazer login (ótimo para ambiente de testes e produção pública).
     - **Contact Information:**
       - O campo será algo como:
         - Developer contact email:
           - Digite novamente o mesmo e-mail (ex: seuemail@gmail.com)
         - Esse é o contato para eventuais notificações do Google sobre a aplicação.
     - **Finish:**
       - Revise as informações e clique em Create (botão azul no canto inferior esquerdo).
       - Isso cria oficialmente a tela de consentimento OAuth.

**✅ Depois que criar**

Você será redirecionado automaticamente para o painel de `OAuth consent screen`. De lá, basta voltar:

 - Ao menu lateral → APIs & Services → Credentials;
 - e aí sim o botão `+ Create credentials` → `OAuth client ID` ficará habilitado.

Agora escolha:

 - **Tipo de aplicativo:**
   - Aplicativo da Web
 - **Nome:**
   - Easy RAG - Django
 - **Em URIs autorizados de redirecionamento, adicione:**
   - http://localhost:8000/accounts/google/login/callback/
        - Se você também utilizar Django em um container: http://localhost/accounts/google/login/callback/
 - **Clique em Criar**
 - Copie o `Client ID` e o `Client Secret`

> **NOTE:**  
> Essas *informações (Client ID e Secret)* serão configuradas no admin do Django, não diretamente no código.

---

### Como pegar as credenciais (chaves) do GitHub

 - Vá em https://github.com/settings/developers
 - Clique em OAuth Apps → New OAuth App
 - Preencha:
   - *Application name:* Easy RAG
   - *Homepage URL:* http://localhost:8000
   - *Authorization callback URL:* http://localhost:8000/accounts/github/login/callback/
 - Clique em `Register Application`
 - Copie o `Client ID`
 - Clique em `Generate new client secret` e copie o `Client Secret`

---

### Adicionando essas credenciais nas variáveis de ambiente (.env)

Tem como utilizar essas credenciais (chaves) diretamente no Django Admin, mas toda vez fazer esse trabalho manualmente pode ser chato.

Uma alternativa é criar essas credenciais (chaves) nas variáveis de ambiente e usa-las na hora de inicialização do projeto (ou seja, quando o container for criado):

[.env](../.env)
```bash
GOOGLE_CLIENT_ID=seu_google_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_google_client_secret_aqui

GITHUB_CLIENT_ID=seu_github_client_id_aqui
GITHUB_CLIENT_SECRET=seu_github_client_secret_aqui
```




















































---

<div id="auto-super-user-and-social-logins"></div>

## `Criando um super usuário e logins sociais automaticamente`

Agora nós vamos implementar alguns script e alterações no nosso código para assim que ele subir nosso container web ele **crie um super usuário** e **configure logins sociais automaticamente**.

De início vamos modificar o nosso [docker-compose.yml](../docker-compose.yml) para não ter aqueles comandos de inicialização:

**ANTES:** [docker-compose.yml](../docker-compose.yml)
```yml
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
```

**AGORA:** [docker-compose.yml](../docker-compose.yml)
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
    volumes:
      - .:/code
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - db
      - redis
    expose:
      - "8000"
    networks:
      - backend

networks:
  backend:
```

[entrypoint.sh](../entrypoint.sh)
```bash
#!/bin/bash
set -e

# ============================================================================
# Configuração de diretórios e permissões
# ============================================================================

setup_directories() {
    # Cria diretórios necessários se não existirem
    mkdir -p /code/media /code/staticfiles

    # Ajusta permissões e ownership dos diretórios
    # Garante que o usuário appuser (UID 1000) possa escrever neles
    chmod -R 755 /code/media /code/staticfiles

    # Obtém o UID do appuser (geralmente 1000)
    APPUSER_UID=$(id -u appuser 2>/dev/null || echo "1000")
    APPUSER_GID=$(id -g appuser 2>/dev/null || echo "1000")

    # Ajusta ownership se estiver rodando como root
    if [ "$(id -u)" = "0" ]; then
        chown -R ${APPUSER_UID}:${APPUSER_GID} \
            /code/media /code/staticfiles 2>/dev/null || true
    fi
}

# ============================================================================
# Funções de inicialização do Django
# ============================================================================

wait_for_postgres() {
    # Aguarda o PostgreSQL estar pronto
    until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
        echo '⏳ Waiting for Postgres...'
        sleep 2
    done
    echo '✅ Postgres is ready!'
}

run_migrations() {
    echo '🔄 Running migrations...'
    python manage.py migrate
}

collect_static_files() {
    echo '📦 Collecting static files...'
    python manage.py collectstatic --noinput
}

create_superuser() {
    echo '👤 Checking for superuser...'
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && \
       [ -n "$DJANGO_SUPERUSER_EMAIL" ] && \
       [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        python manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(
    username="${DJANGO_SUPERUSER_USERNAME}"
).exists():
    User.objects.create_superuser(
        "${DJANGO_SUPERUSER_USERNAME}",
        "${DJANGO_SUPERUSER_EMAIL}",
        "${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("✅ Superuser created successfully!")
else:
    print("ℹ️  Superuser already exists, skipping creation.")
PYEOF
    else
        echo '⚠️  Superuser environment variables not set, ' \
             'skipping superuser creation.'
    fi
}

setup_social_providers() {
    echo '🔐 Setting up social providers...'
    python manage.py setup_social_providers
}

start_django_server() {
    echo '🚀 Starting Django server...'
    exec python manage.py runserver \
        ${DJANGO_HOST:-0.0.0.0}:${DJANGO_PORT:-8000}
}

# ============================================================================
# Inicialização completa do Django
# ============================================================================

init_django() {
    wait_for_postgres
    run_migrations
    collect_static_files
    create_superuser
    setup_social_providers
    start_django_server
}

# ============================================================================
# Script principal
# ============================================================================

main() {
    # Configura diretórios e permissões
    setup_directories

    # Se estiver rodando como root
    if [ "$(id -u)" = "0" ]; then
        # Se não houver comando passado ou se for o comando padrão/bash,
        # executa inicialização completa
        if [ $# -eq 0 ] || [ "$1" = "bash" ]; then
            # Executa a inicialização como appuser usando heredoc
            # para preservar o contexto das funções
            exec gosu appuser bash << 'INIT_SCRIPT'
set -e

# Aguarda o PostgreSQL estar pronto
until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  echo '⏳ Waiting for Postgres...'
  sleep 2
done

echo '✅ Postgres is ready!'

# Executa migrations
echo '🔄 Running migrations...'
python manage.py migrate

# Coleta arquivos estáticos
echo '📦 Collecting static files...'
python manage.py collectstatic --noinput

# Cria super usuário se não existir
echo '👤 Checking for superuser...'
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && \
   [ -n "$DJANGO_SUPERUSER_EMAIL" ] && \
   [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(
    username="${DJANGO_SUPERUSER_USERNAME}"
).exists():
    User.objects.create_superuser(
        "${DJANGO_SUPERUSER_USERNAME}",
        "${DJANGO_SUPERUSER_EMAIL}",
        "${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("✅ Superuser created successfully!")
else:
    print("ℹ️  Superuser already exists, skipping creation.")
PYEOF
else
  echo '⚠️  Superuser environment variables not set, ' \
       'skipping superuser creation.'
fi

# Configura provedores sociais
echo '🔐 Setting up social providers...'
python manage.py setup_social_providers

# Inicia o servidor
echo '🚀 Starting Django server...'
exec python manage.py runserver \
    ${DJANGO_HOST:-0.0.0.0}:${DJANGO_PORT:-8000}
INIT_SCRIPT
        else
            # Executa o comando passado como appuser
            exec gosu appuser "$@"
        fi
    else
        # Se já estiver rodando como appuser e não houver comando,
        # executa inicialização
        if [ $# -eq 0 ] || [ "$1" = "bash" ]; then
            init_django
        else
            # Executa o comando passado
            exec "$@"
        fi
    fi
}

# Executa o script principal
main "$@"
```

> **E aqueles comandos, onde (em que parte do código) serão executados?**

 - **ONDE ESTÃO SENDO EXECUTADOS:**
   - Os comandos agora estão executados no [entrypoint.sh](../entrypoint.sh).
 - **EM QUE PARTE DO CÓDIGO:**
   - O [entrypoint.sh](../entrypoint.sh) é executado automaticamente quando o container inicia, porque:
     - No [Dockerfile](../Dockerfile), o ENTRYPOINT está definido como ["/entrypoint.sh"] (linha 54 do Dockerfile).
     - No [docker-compose.yml](../docker-compose.yml), o serviço web não tem um command: definido (foi removido).
     - Quando não há **command:** no docker-compose, o Docker usa o *CMD* do [Dockerfile](../Dockerfile), que é ["bash"] (linha 69 do Dockerfile).

> **NOTE:**  
> Mas nós ainda não estamos criando um super usuário e nem configurando os logins sociais.

Para resolver o problema citado acima nós vamos criar um script python para fazer isso automaticamente:

[users/management/commands/setup_social_providers.py](../users/management/commands/setup_social_providers.py)
```python
import os

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Configura provedores sociais (Google e GitHub) a partir de '
        'variáveis de ambiente'
    )

    def handle(self, *args, **options):
        site_id = int(os.getenv("DJANGO_SITE_ID", "1"))
        site_domain = os.getenv(
            "DJANGO_SITE_DOMAIN", "localhost:8000"
        )
        site_name = os.getenv("DJANGO_SITE_NAME", "localhost")

        try:
            site = Site.objects.get(id=site_id)
            # Atualiza o site se ainda estiver com valores padrão
            if site.domain != site_domain or site.name != site_name:
                site.domain = site_domain
                site.name = site_name
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} atualizado: '
                        f'domain="{site_domain}", name="{site_name}"'
                    )
                )
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Site com ID {site_id} não encontrado. Criando...'
                )
            )
            site = Site.objects.create(
                id=site_id,
                domain=site_domain,
                name=site_name
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Site {site_id} criado: '
                    f'domain="{site_domain}", name="{site_name}"'
                )
            )

        # Configurar Google
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if google_client_id and google_client_secret:
            social_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': google_client_id,
                    'secret': google_client_secret,
                }
            )

            if not created:
                # Atualiza se já existir
                social_app.client_id = google_client_id
                social_app.secret = google_client_secret
                social_app.save()
                self.stdout.write(
                    self.style.WARNING('SocialApp Google atualizado.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'SocialApp Google criado com sucesso.'
                    )
                )

            # Garante que o site está associado
            if site not in social_app.sites.all():
                social_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} associado ao Google.'
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis GOOGLE_CLIENT_ID ou '
                    'GOOGLE_CLIENT_SECRET não encontradas. '
                    'Pulando configuração do Google.'
                )
            )

        # Configurar GitHub
        github_client_id = os.getenv("GITHUB_CLIENT_ID")
        github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

        if github_client_id and github_client_secret:
            social_app, created = SocialApp.objects.get_or_create(
                provider='github',
                defaults={
                    'name': 'GitHub',
                    'client_id': github_client_id,
                    'secret': github_client_secret,
                }
            )

            if not created:
                # Atualiza se já existir
                social_app.client_id = github_client_id
                social_app.secret = github_client_secret
                social_app.save()
                self.stdout.write(
                    self.style.WARNING('SocialApp GitHub atualizado.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'SocialApp GitHub criado com sucesso.'
                    )
                )

            # Garante que o site está associado
            if site not in social_app.sites.all():
                social_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} associado ao GitHub.'
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis GITHUB_CLIENT_ID ou '
                    'GITHUB_CLIENT_SECRET não encontradas. '
                    'Pulando configuração do GitHub.'
                )
            )
```

Ótimo, agora é só recriar os containers novamente que ele automaticamente vai criar:

 - Um super usuário;
 - Configurar os logins sociais.

```bash
task build_compose
```







































































































---

<div id="linking-social-buttons"></div>

## `Linkando os botões de login social`

 - Até aqui, nós configuramos o `django-allauth` para registrar os provedores (Google e GitHub) no painel administrativo.
 - Agora, nós vamos fazer com que os botões **“Entrar com Google”** e **“Entrar com GitHub”** funcionem de verdade, conectando o *front-end* com o *allauth*.

[templates/pages/index.html](../templates/pages/index.html)
```html
{% load socialaccount %}


<!-- Botão de Login com Google -->
<div>
    <a href="{% provider_login_url 'google' %}"
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
    <a href="{% provider_login_url 'github' %}"
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
```

**Explicação das principais partes do código:**

**🧩 Herança do template e carregamento de tags**
```html
{% load socialaccount %}
```

 - `{% load socialaccount %}`
   - Importa os templates tags fornecidas pelo `django-allauth (ex.: {% provider_login_url %})`.
   - Sem esse `load`, as tags sociais nao seriam reconhecidas pelo template engine.

**🧩 Botões de login social (links gerados pelo allauth)**
```html
<a href="{% provider_login_url 'google' %}">
    ...
</a>

<a href="{% provider_login_url 'github' %}">
    ...
</a>
```

 - **O que faz?**
   - `{% provider_login_url 'google' %}` e `{% provider_login_url 'github' %}`
     - Geram as URLs corretas para iniciar o fluxo `OAuth` com *Google* e *GitHub* (fornecidas pelo django-allauth).
     - Os `<a>` envolvem botões visuais que, ao clicar, redirecionam o usuário para o provedor externo.
 - **Por que é importante?**
   - Conecta o front-end ao sistema de login social do allauth.
   - O allauth cuida de gerar a URL correta, adicionar parâmetros e tratar callbacks.

Agora quando você clicar para logar com o **Google** ou **GitHub** você será redirecionado para o provedor externo, onde ele irá perguntar ao usuário se ele quer permitir o acesso ao seu perfil ou não:

![img](images/social-login-01.png)  

**NOTE:**  
Porém, nesse exemplo acima nós não somos redirecionados diretamente para os provedores externos do google e github respectivamente. Primeiro, nós passamos por páginas internas do allauth e depois redirecionamos para eles.

> **Tem como ir diretor para os provedores externos do Google e GitHub sem passar por essas páginas do allauth?**

**SIM!**  
Para isso nós precisamos configurar [settings.py](../core/settings.py) para que o allauth redirecione diretamente para os provedores externos:

[core/settings.py](../core/settings.py)
```python
SOCIALACCOUNT_LOGIN_ON_GET = True
```

 - `SOCIALACCOUNT_LOGIN_ON_GET = True`
   - Quando `True`, o allauth redireciona diretamente para o provedor externo ao clicar nos botões de login.
   - **NOTE:** Por padrão, ele vem como `False`.








































































































---

<div id="rewriting-allauth-messages"></div>

## `Reescrevendo as mensagens do Django Allauth`

Continuando, aqui nós temos um probleminha, quando nós deslogamos com alguma das contas sociais aparece uma mensagem na nossa página principal (langin page):

![img](images/social-login-02.png)  

É como se fosse o *"resto"* de uma mensagem do Django depois do login!

> **Como resolver isso?**

#### Criando um `adapter.py`

O arquivo [adapter.py](../users/adapter.py) serve para *personalizar o comportamento interno do Django Allauth*, que é o sistema responsável pelos *logins*, *logouts* e *cadastros* — tanto locais quanto via provedores sociais (como Google e GitHub).

Por padrão, o Allauth envia automaticamente mensagens para o sistema de mensagens do Django (django.contrib.messages), exibindo textos como:

 - “Successfully signed in as rodrigols89.”
 - “You have signed out.”
 - “Your email has been confirmed.”

Essas mensagens são geradas dentro dos adapters do `Allauth` — classes que controlam como ele interage com o Django.

Agora, vamos criar (recriar) nossas versões personalizadas dos adapters (`NoMessageAccountAdapter` e `NoMessageSocialAccountAdapter`) para impedir que essas mensagens automáticas sejam exibidas.

> **NOTE:**  
> Assim, temos controle total sobre quais mensagens aparecem para o usuário — mantendo o front mais limpo e sem textos gerados automaticamente.

[users/adapter.py](../users/adapter.py)
```python
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter
)


class NoMessageAccountAdapter(DefaultAccountAdapter):
    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None
    ):
        return


class NoMessageSocialAccountAdapter(DefaultSocialAccountAdapter):
    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None
    ):
        return
```

Por fim, vamos adicionar algumas configurações gerais em `settings.py`:

[settings.py](../core/settings.py)
```python
ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapter.NoMessageSocialAccountAdapter"
```

 - Use o caminho Python completo para a classe.
 - No exemplo acima assumimos que:
   - O app se chama `users`;
   - No arquivo `adapter`;
   - Estamos chamando as classes: `NoMessageAccountAdapter` e `NoMessageSocialAccountAdapter`.

Por fim, reinicie o servidor (python manage.py runserver) depois de editar `settings.py` para que as mudanças tenham efeito.









































































































---

<div id="app-workspace"></div>

## `Criando o app "workspace"`

> Aqui vamos criar um app Django dedicado ao *Workspace (onde o usuário poderá criar pastas e fazer upload de arquivos)* e registrar esse app nas configurações do projeto.

**SE VOCÊ CRIAR DIRETAMENTE DO CONTAINER NÃO VAI TER PERMISSÕES LOCAIS:**
```bash
python manage.py startapp workspace
```

**AGORA VAMOS REINICIAR O CONTAINER PARA ESSA ALTERAÇÃO REFLETIR NO CONTAINER:**
```bash
task restart_compose
```

Agora vamos registrar esse app nas configurações do projeto:

[settings.py](../core/settings.py)
```python
INSTALLED_APPS = [

    ...

    # Seus apps
    "users",
    "workspace",
]
```









































































































---

<div id="home-to-workspace"></div>

## `Mapeando a rota home/ com a workspace/`

> Aqui nós vamos relacionar o template `home.html` com o template `workspace.html`.

De início vamos fazer nosso projeto reconhecer as URLs do App `workspace`:

[core/urls.py](../core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),
    path(
        "accounts/",
        include("allauth.urls")
    ),
    path(
        "",
        include("users.urls")
    ),
    path(
        "",
        include("workspace.urls")
    ),
]
```

Agora nós vamos criar uma URL específica para a rota `/workspace/`:

[workspace/urls.py](../workspace/urls.py)
```python
from django.urls import path

from . import views

urlpatterns = [
    path(
        route="workspace/",
        view=views.workspace_home,
        name="workspace_home"
    ),
]
```

Continuando, agora vamos atualizar nosso [sidebar.html](../templates/partials/sidebar.html) para:

 - Quando alguém clicar em "Workspace" ele seja redirecionado para `/workspace/`;
 - QUando alguém clicar em "Home" ele seja redirecionado para `/home/`;

[sidebar.html](../templates/partials/sidebar.html)
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
               href="{% url 'workspace_home' %}">
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

Agora nós precisamos criar uma view (ação) para:

- Quando alguém clicar no botão (link) **"Workspace"** em `home.html`, seja redirecionado para `workspace_home.html`;
 - E essa pessoa também tem que estar logada para acessar essa rota.

[workspace/views.py](../workspace/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/")
def workspace_home(request):
    return render(request, "pages/workspace_home.html")
```

Continuando, vou mostrar como vai ficar nosso `workspace.html (versão inicial)` (como HTML e CSS não é nosso foco vamos ignorar isso por enquanto):

[workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
{% extends "base.html" %}

{% block title %}Workspace{% endblock %}

{% block content %}
    <div class="flex h-screen bg-gray-100">

        <!-- 🧱 Sidebar -->
        {% include "partials/sidebar.html" with current_page="workspace" %}

    </div>
{% endblock %}
```









































































































---

<div id="modeling-folder-file"></div>

## `Modelando o workspace: Pastas (Folders) e Arquivos (Files)`

Nesta etapa vamos modelar o **núcleo do Workspace**:

 - Pastas (Folder);
 - Arquivos (File).
 - **NOTE:** Também incluiremos uma função `workspace_upload_to()` para organizar os arquivos no disco por usuário e pasta.

### `Função workspace_upload_to()`

Vamos começar entendo a função `workspace_upload_to()` é usada pelo Django para definir dinamicamente o caminho onde um arquivo será salvo dentro do MEDIA_ROOT.

Ela é passada como valor do parâmetro `upload_to` em um `FileField`, permitindo que o caminho do arquivo dependa de:

 - Quem fez o upload (usuário);
 - Em qual pasta do workspace o arquivo está;
 - Nome do arquivo tratado de forma segura.

Em vez de salvar tudo em um diretório fixo, essa função cria uma estrutura hierárquica organizada, por exemplo:

```bash
media/
└── workspace/
    └── user_3/
        └── folder_12/
            └── contrato.pdf
```

Agora, vamos implementar a função `workspace_upload_to()` na prática:

[workspace/models.py](../workspace/models.py)
```python
import os
import re


def workspace_upload_to(instance, filename):
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
```

A função recebe dois parâmetros:

 - `instance`
   - Instância do modelo *File* sendo salvo (Django).
 - `filename`
   - Nome original do arquivo enviado.

Esses parâmetros vêm do Django quando um arquivo é enviado via *FileField* ou *ImageField* com `upload_to=workspace_upload_to`.

```bash
try:
    # Linha 25-28: Verifica se instance.folder existe E se tem owner E se owner existe E se owner tem id
    if (instance.folder and
        hasattr(instance.folder, 'owner') and
        instance.folder.owner and
        hasattr(instance.folder.owner, 'id')):
        # Linha 29: Se tudo estiver OK, cria user_part com o ID do dono da pasta
        user_part = f"user_{instance.folder.owner.id}"
    # Linha 30-31: Se não tiver folder.owner, tenta pegar direto do instance.uploader
    elif hasattr(instance, 'uploader') and instance.uploader:
        user_part = f"user_{instance.uploader.id}"
    # Linha 32-33: Se não tiver nem folder.owner nem uploader, usa user_0 como padrão
    else:
        user_part = "user_0"
except (AttributeError, ValueError):
    # Linha 35-36: Se deu erro no try acima, tenta pegar direto do instance.uploader
    try:
        user_part = f"user_{instance.uploader.id}"
    # Linha 37-38: Se mesmo assim der erro, usa user_0 como fallback final
    except (AttributeError, ValueError):
        user_part = "user_0"
```

 - **Quando entra no try?**
   - Quando `instance` tem os atributos esperados e não há erros ao acessá-los.
 - **Quando entra no except?**
   - Quando ocorre AttributeError (atributo não existe) ou ValueError (valor inválido) ao acessar `instance.folder`, `instance.folder.owner`, `instance.folder.owner.id`, etc.

```bash
try:
    # Linha 41-43: Verifica se instance.folder existe E se tem id E se o id não é None/vazio
    if (instance.folder and
            hasattr(instance.folder, 'id') and
            instance.folder.id):
        # Linha 44: Se tiver folder com id, cria folder_part com o ID da pasta
        folder_part = f"folder_{instance.folder.id}"
    # Linha 45-46: Se não tiver folder ou folder.id, usa "root" (pasta raiz)
    else:
        folder_part = "root"
except (AttributeError, ValueError):
    # Linha 48: Se der qualquer erro, assume que é pasta raiz
    folder_part = "root"
```

 - **Quando entra no try?**
   - Quando `instance` tem os atributos esperados e não há erros ao acessá-los.
 - **Quando entra no except?**
   - Quando ocorre *AttributeError* ou *ValueError* ao acessar `instance.folder` ou `instance.folder.id`.

```bash
safe_name = os.path.basename(filename)
safe_name = re.sub(r'[<>:"|?*\x00-\x1f]', '_', safe_name)
safe_name = safe_name.strip()
```

 - `safe_name = os.path.basename(filename)`
   - `os.path.basename`
     - Função da biblioteca padrão os.
     - Remove qualquer caminho do nome do arquivo.
     - Exemplo: `"pasta/arquivo.txt" → "arquivo.txt"`
 - `safe_name = re.sub(r'[<>:"|?*\x00-\x1f]', '_', safe_name)`
   - `re.sub`
     - Biblioteca *re (regex)*.
     - Substitui caracteres inválidos para sistemas de arquivos por `_`.
 - `safe_name = safe_name.strip()`
   - Remove espaços no início e no fim.

```bash
if not safe_name:
    safe_name = "unnamed-file"
```

 - Garante que o nome nunca seja vazio.
 - Evita erros de sistema operacional.

```bash
return os.path.join("workspace", user_part, folder_part, safe_name)
```

 - `os.path.join`
   - Junta caminhos respeitando o sistema operacional.
   - Exemplo final: `workspace/user_3/folder_12/contrato.pdf`

### `Classe Folder()`

A classe `Folder` representa uma **pasta virtual dentro do workspace do usuário**, permitindo:

 - Estrutura hierárquica (pastas dentro de pastas);
 - Associação direta com um usuário (dono);
 - Soft delete (exclusão lógica);
 - Organização cronológica;
 - Base para upload de arquivos e RAG futuramente.

Ela funciona como uma árvore (tree structure), onde cada pasta pode ter:

 - um pai (parent);
 - vários filhos (children).

[workspace/models.py](../workspace/models.py)
```python
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Folder(models.Model):

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
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

**📌 Campo: name**
```python
name = models.CharField(
    _("name"),
    max_length=255
)
```

 - **O que é?**
   - Campo que armazena o nome da pasta.
 - **Detalhes técnicos:**
   - `models.CharField`
     - Campo de texto curto no banco de dados.
   - `_("name")`
     - Usa tradução internacional (i18n) do Django.
     - `_()` vem de django.utils.translation.
     - Permite traduzir o nome do campo no admin e formulários.
   - `max_length=255`
     - Limita o tamanho do nome.
     - Compatível com praticamente todos os bancos (Postgres, MySQL, SQLite).

**👤 Campo: owner**
```python
owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="folders",
)
```

 - **O que é?**
   - Define quem é o dono da pasta.
 - **Detalhes técnicos:**
   - `models.ForeignKey(...)`
     - Relacionamento muitos-para-um:
       - Um usuário pode ter várias pastas;
       - Cada pasta pertence a um usuário.
   - `settings.AUTH_USER_MODEL`
     - Referência ao modelo de usuário ativo do projeto;
     - Pode ser *auth.User* ou um usuário customizado;
     - Boa prática absoluta (evita acoplamento).
   - `on_delete=models.CASCADE`
     - Se o usuário for excluído:
       - Todas as pastas dele serão excluídas automaticamente.
   - `related_name="folders"`
     - Permite acessar: *user.folders.all()*
 - **📌 Importante:**
   - Esse campo é essencial para segurança, isolamento de dados e multi-tenant.

**🌳 Campo: parent**
```python
parent = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    related_name="children",
)
```

 - **O que é?**
   - Permite criar pastas dentro de pastas.
 - **Detalhes técnicos:**
   - `self`
     - O relacionamento aponta para o próprio modelo Folder.
   - `null=True`
     - No banco de dados:
       - Permite NULL;
       - Usado para pastas raiz (sem pai).
   - `blank=True`
     - Em formulários:
       - Campo opcional.
   - `on_delete=models.CASCADE`
     - Se uma pasta pai for deletada:
       - Todas as subpastas são deletadas junto.
   - `related_name="children"`
     - Permite acessar: *folder.children.all()*

**🕒 Campos de controle e soft delete:**
```python
created_at = models.DateTimeField(auto_now_add=True)
is_deleted = models.BooleanField(default=False)
deleted_at = models.DateTimeField(null=True, blank=True)
```

 - `created_at = models.DateTimeField(auto_now_add=True)`
   - Salva automaticamente a data/hora de criação.
   - Nunca muda depois de criada.
   - Ideal para:
     - ordenação;
     - auditoria;
     - histórico.
 - `is_deleted = models.BooleanField(default=False)`
   - Implementa soft delete;
   - A pasta não é removida do banco;
   - Apenas marcada como deletada.
   - 📌 Vantagens:
     - Recuperação futura;
     - Auditoria;
     - Evita perda acidental.
 - `deleted_at = models.DateTimeField(null=True, blank=True)`
   - Guarda *quando* a pasta foi deletada.
   - Usado junto com is_deleted.
   - Permite:
     - lixeira;
     - limpeza agendada;
     - versionamento.

```python
class Meta:
    ordering = ["-created_at"]
    verbose_name = _("Folder")
    verbose_name_plural = _("Folders")
```

 - `ordering = ["-created_at"]`
   - Define ordenação padrão das queries:
     - Mais recentes primeiro.
 - `verbose_name = _("Folder")`
   - Nome legível do modelo;
   - Usado no Django Admin e formulários;
   - Traduzível.
 - `verbose_name_plural = _("Folders")`
   - Forma plural correta.
   - Evita: *Folder s*

```python
def __str__(self):
    """Representação em string do modelo."""
    return self.name
```

 - **Para que serve?**
   - Define como o objeto aparece quando convertido para string:
     - Django Admin;
     - Shell (print(folder));
     - Logs;
     - Debug.

### `Classe File()`

A classe **File** representa um arquivo físico armazenado no workspace do usuário, podendo:

 - Estar dentro de uma pasta (Folder);
 - Ou estar na raiz do workspace;
 - Ser associado a um usuário específico;
 - Ser organizado cronologicamente;
 - Ser excluído logicamente (soft delete).

> **NOTE:**  
> Ela é o **modelo que conecta o mundo físico (filesystem)** com o mundo **lógico (banco de dados)**.

[models.py](../workspace/models.py)
```python
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
```

### `Continuando com a modelagem do App workspace`

Agora, vamos criar as migrações do App `workspace` e do Banco de Dados geral:

```bash
docker compose exec web python manage.py makemigrations workspace
```

```bash
docker compose exec web python manage.py migrate
```

> **Mas como eu posso testar se está funcionando manualmente?**

Primeiro, nós podemos adicionar (registrar) essas modelagens no nosso [admin.py](../workspace/admin.py):

[admin.py](../workspace/admin.py)
```python
from django.contrib import admin
from .models import Folder, File


admin.site.register(Folder)
admin.site.register(File)
```

Agora se você atualizar a página no seu Django Admin verá:

![img](images/workspace-01.png)  

Ou seja, o projeto `workspace` tem os modelos:

 - `Files`;
 - `Folders`.

Agora, podemos criar alguns folders e adicionar alguns arquivos:

![img](images/workspace-00.png)  

![img](images/workspace-02.png)  

![img](images/workspace-03.png)  

Vejam que:

 - **As *Pastas (Folders)* seguem uma estrutura em árvore:**
   - Tem que ter um dono (`owner`);
   - Se tiver uma pasta pai (`parent`) selecione ela:
     - Se não tiver essa pasta vai para a raiz.
   - **NOTE:** Também é obrigatório escolher um nome para a pasta.
 - **Os *Arquivos (Files)* estão sendo relacionados:**
   - Uma *Pasta (Folder)*;
   - Um *Usuário (Uploader)*.
   - **NOTE:** Também é obrigatório escolher um nome para o arquivo.

> **Onde estão essas pastas/arquivos no nosso projeto?**  
> Em `media/` e separado por usuarios.

![img](images/workspace-04.png)  

> **Mas esses dados também estão sendo salvos no Banco de Dados (PostgreSQL)?**

Vamos abrir nosso Banco de Dados PostgreSQL para verificar:

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
 Schema |             Name              | Type  |  Owner  | Persistence | Access method |    Size    | Description
--------+-------------------------------+-------+---------+-------------+---------------+------------+-------------
 public | workspace_file                | table | easyrag | permanent   | heap          | 8192 bytes |
 public | workspace_folder              | table | easyrag | permanent   | heap          | 8192 bytes |
```

> **NOTE:**  
> Vejam que nós temos as tabelas `workspace_file` e `workspace_folder`.

Por fim, vamos listar quantas *Pastas (Folders)* e *Arquivos (Files)* temos cadastrados no Banco de Dados:

**Lista quantas pastas (folders) temos cadastradas:**
```bash
select * from workspace_folder;



 id |    name     |          created_at           | owner_id | parent_id
----+-------------+-------------------------------+----------+-----------
  1 | Dota2       | 2025-11-16 20:25:52.853803+00 |        1 |
  2 | Mathematics | 2025-11-16 20:26:01.732653+00 |        2 |
  3 | RAG         | 2025-11-16 20:26:13.053282+00 |        1 |
  4 | Physics     | 2025-11-16 20:26:22.719736+00 |        1 |
(4 rows)
```

**Lista quantos arquivos (files) temos cadastrados:**
```bash
select * from workspace_file;



 id |        name         |                                                 file                                                 |          uploaded_at          | uploader_id | folder_id
----+---------------------+------------------------------------------------------------------------------------------------------+-------------------------------+-------------+-----------
  1 | Physics - Exercises | workspace/user_1/folder_4/Physics.pdf                                                                | 2025-11-16 20:34:30.137585+00 |           1 |         4
  2 | Math - Exercises    | workspace/user_2/folder_2/Math.pdf                                                                   | 2025-11-16 20:35:32.587887+00 |           1 |         2
  3 | RAG - Exercises     | workspace/user_1/folder_3/RAG_Retrieval_Augmented_Generation_Aplicado_à_Ciência_de_Dados.pdf         | 2025-11-16 20:39:10.916045+00 |           1 |         3
  4 | Dota2 - DRL         | workspace/user_1/folder_1/Applications_of_Machine_Learning_in_Dota_2_-_Literature_Review_pcINztR.pdf | 2025-11-16 20:41:56.880436+00 |           1 |         1
(4 rows)
```









































































































---

<div id="workspace-forms"></div>

## `Customizando os formulários FolderForm e FileForm`

Agora vamos implementar (customizar) os formulários `FolderForm` e `FileForm` do app workspace, responsáveis por coletar dados do usuário de maneira segura e validada.

> **Mas isso é realmente necessário?**

Para entender isso vamos começar com um resumo de diferença entre as modelagens `Folder` e `File` e os formulários (customizados) `FolderForm` e `FileForm`:

| Parte                                | O que faz?                                                           | Salva no banco?                        | Onde é usada?                          |
| ------------------------------------ | -------------------------------------------------------------------- | -------------------------------------- | -------------------------------------- |
| **Models** (`Folder`, `File`)        | Define a estrutura das tabelas no banco e como os dados são salvos.  | Sim                                    | Banco de dados (via ORM)               |
| **Forms** (`FolderForm`, `FileForm`) | Define como os dados são capturados e validados na interface (HTML). | Não diretamente (precisa de `.save()`) | Interface do usuário (views/templates) |

Bem, entendendo isso vamos partir para a implementação (customização) dos nossos formulários:

[forms.py](../workspace/forms.py)
```python
from django import forms
from django.core.exceptions import ValidationError

from .models import File, Folder


def validate_file_size(value):

    max_mb = 100
    max_bytes = max_mb * 1024 * 1024

    if value.size > max_bytes:
        raise ValidationError(
            f"O arquivo não pode ser maior que {max_mb} MB."
        )


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full px-3 py-2 border rounded",
                    "placeholder": "Nome da pasta",
                }
            ),
        }
        error_messages = {
            "name": {
                "required": "O nome da pasta é obrigatório."
            },
        }

    def clean_name(self):

        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise ValidationError("Nome inválido.")

        return name


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["name", "file"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full px-3 py-2 border rounded",
                    "placeholder": "Nome do arquivo (opcional)",
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={"class": "block w-full"}
            ),
        }
        error_messages = {
            "file": {
                "required": "Selecione um arquivo para enviar."
            },
        }

    file = forms.FileField(validators=[validate_file_size])

    def clean_name(self):

        name = self.cleaned_data.get("name")
        uploaded = self.cleaned_data.get("file")

        if not name and uploaded:
            return uploaded.name

        return name


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["file"]
```









































































































---

<div id="update-view-to-list-folders-and-files"></div>

## `Atualizando a view (ação) para exibir as pastas e arquivos`

> **NOTE:**  
> Antes de implementar essa funcionalidade (feature) é importante que você crie algumas pastas e faça upload de alguns arquivos nessas pastas a partir do *Django Admin*.

Continuando, lembram que nós tinhamos uma view (ação) só para exibir a página `workspace_home.html`?

[workspace/views.py](../workspace/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/")
def workspace_home(request):
    return render(request, "pages/workspace_home.html")
```

Então, agora nós vamos atualizar essa view (ação) para:

 - Listar as pastas e arquivos do usuário logado;
 - Mostrar somente o conteúdo que pertence a ele (usando request.user);
 - Servir como a página principal do Workspace, onde futuramente adicionaremos botões para *“criar pasta”* e *“fazer upload”*.

Vamos começar atualizando a view (ação) `workspace_home()`:

[views.py](../workspace/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import File, Folder


@login_required(login_url="/")
def workspace_home(request):

    folder_id = request.GET.get("folder")

    if folder_id:
        current_folder = get_object_or_404(
            Folder,
            id=folder_id,
            owner=request.user
        )

        folders = Folder.objects.filter(
            parent=current_folder,
            owner=request.user,
            is_deleted=False
        ).order_by("name")

        files = File.objects.filter(
            folder=current_folder,
            uploader=request.user,
            is_deleted=False
        ).order_by("name")

        breadcrumbs = []
        temp = current_folder
        while temp:
            breadcrumbs.append(temp)
            temp = temp.parent
        breadcrumbs.reverse()

    else:
        current_folder = None

        folders = Folder.objects.filter(
            owner=request.user,
            parent__isnull=True,
            is_deleted=False
        ).order_by("name")

        files = File.objects.filter(
            uploader=request.user,
            folder__isnull=True,
            is_deleted=False
        ).order_by("name")

        breadcrumbs = []

    context = {
        "current_folder": current_folder,
        "folders": folders,
        "files": files,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "pages/workspace_home.html", context)
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
folder_id = request.GET.get("folder")
```

 - **O que essa linha faz?**
   - Ela lê um parâmetro da URL (query string) chamado folder.
   - Exemplos de URL:
     - `/workspace` → folder_id = None
     - `/workspace?folder=5` → folder_id = "5"
 - **📌 Ou seja:**
   - Serve para saber em qual pasta o usuário está navegando;
   - Controla a navegação hierárquica do workspace
 - **⚠️ Importante:**
   - O valor vem como string;
   - Não faz validação aqui (isso será feito depois).

```python
if folder_id:
    ..
else:
    ..
```

 - **Quando entra no if?**
   - O usuário clicou em uma pasta;
   - A URL contém `?folder=<id>`;
   - Exemplo: `/workspace?folder=12`
 - **Quando entra no else?**
   - folder_id é None;
   - Ou seja: não há pasta selecionada;
   - O usuário está na raiz.

```python
current_folder = get_object_or_404(
    Folder,
    id=folder_id,
    owner=request.user
)
```

 - **O que esse bloco faz?**
   - Busca uma pasta específica.
   - Garante que:
     - ela existe;
     - pertence ao usuário logado.
   - Se não existir → retorna 404 automaticamente
 - `get_object_or_404()`
   - Função do Django que:
     - Executa uma query;
     - Se encontrar → retorna o objeto;
     - Se não encontrar → lança um Http404.
   - *Argumentos que ela recebe:*
     - `Folder` → o modelo;
     - `id=folder_id` → garante que é a pasta correta;
     - `owner=request.user` → garante que pertence ao usuário logado, segurança (um usuário não acessa pasta de outro).

```python
folders = Folder.objects.filter(
    parent=current_folder,
    owner=request.user,
    is_deleted=False
).order_by("name")
```

 - **O que esse bloco faz?**
   - Busca as subpastas da pasta atual.
 - `Folder.objects.filter(...)`
   - Query no modelo *"Folder"*.
   - **Argumentos explicados:**
     - `parent=current_folder`
       - só pastas filhas da pasta atual.
     - `owner=request.user`
       - Só pastas do usuário logado.
     - `is_deleted=False`
       - Ignora pastas excluídas logicamente (soft delete).

```python
files = File.objects.filter(
    folder=current_folder,
    uploader=request.user,
    is_deleted=False
).order_by("name")
```

 - **O que esse bloco faz?**
   - Busca os arquivos dentro da pasta atual.
 - `File.objects.filter(...)`
   - Query no modelo *"File"*.
   - **Argumentos explicados:**
     - `folder=current_folder`
       - Arquivos que pertencem à pasta atual.
     - `uploader=request.user`
       - Arquivos do usuário logado.
     - `is_deleted=False`
       - Ignora arquivos excluídos (soft delete).
     - `.order_by("name")`
       - Ordena alfabeticamente.

```python
breadcrumbs = []
temp = current_folder
while temp:
    breadcrumbs.append(temp)
    temp = temp.parent
breadcrumbs.reverse()
```

 - **O que esse bloco faz?**
   - Constrói o caminho hierárquico da pasta atual até a raiz (breadcrumb).
   - 📁 Exemplo: *Raiz / Pasta 1 / Pasta 2 / Pasta 3*
 - `breadcrumbs = []`
   - Lista vazia que vai armazenar as pastas.
 - `temp = current_folder`
   - Variável temporária para navegar na hierarquia.
 - `while temp:`
   - Enquanto existir uma pasta (até chegar na raiz).
   - `breadcrumbs.append(temp)`
     - Adiciona a pasta atual à lista.
   - `temp = temp.parent`
     - Sobe um nível na hierarquia.
 - `breadcrumbs.reverse()`
   - Inverte a lista para ficar da raiz → pasta atual.

**No else:**
```python
current_folder = None
```

 - **O que ela significa?**
   - Indica explicitamente:
     - O usuário está na raiz;
     - Não há pasta selecionada.

```python
folders = Folder.objects.filter(
    owner=request.user,
    parent__isnull=True,
    is_deleted=False
).order_by("name")
```

 - **O que esse bloco faz?**
   - Busca todas as pastas da raiz do usuário.
 - `Folder.objects.filter(...)`
   - Query no modelo *"Folder"*.

```python
files = File.objects.filter(
    uploader=request.user,
    folder__isnull=True,
    is_deleted=False
).order_by("name")
```

 - **O que esse bloco faz?**
   - Busca arquivos que estão soltos na raiz, sem pasta.
 - `File.objects.filter(...)`
   - Query no modelo *"File"*.

```python
breadcrumbs = []
```

 - **O que essa linha faz?**
   - Indica que:
     - Não há caminho hierárquico;
     - O usuário está na raiz.

```python
context = {
    "current_folder": current_folder,
    "folders": folders,
    "files": files,
    "breadcrumbs": breadcrumbs,
}
```

 - **O que esse bloco faz?**
   - Cria o contexto que será enviado ao template.

```python
return render(request, "pages/workspace_home.html", context)
```

 - **O que essa linha (retorno) faz?**
   - Renderiza o template HTML;
   - Injeta o context;
   - Retorna um HttpResponse;
   - 📌 Esse é o retorno final da view.

### Continuando...

Continuando, vamos começar atualizando nosso template [workspace_home.html](../workspace/templates/pages/workspace_home.html) para exibir qual usuário está logado:

[workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
{% extends "base.html" %}

{% block title %}Workspace{% endblock %}

{% block content %}
    <div class="flex h-screen bg-gray-100">

        <!-- 🧱 Sidebar -->
        {% include "partials/sidebar.html" with current_page="workspace" %}

        <!-- 💼 Área principal do Workspace -->
        <main class="flex-1 p-8 overflow-y-auto">

            <!-- Header -->
            <header class="bg-white shadow px-6 py-4">
                <h1 class="text-2xl font-semibold text-gray-800">
                    Bem-vindo, {{ request.user.username }}!
                </h1>
            </header>

        </main>
    </div>
{% endblock %}
```

Agora, vamos fazer nosso template lista as pastas e arquivos que o usuário logado tem (lembrando que nós criamos essas pastas e arquivos a partir do Django Admin):

[workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<!-- 📁 Listagem mista de pastas e arquivos -->
{% if folders or files %}
    <ul class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4
        gap-4">

        <!-- Pastas -->
        {% for folder in folders %}
            <li class="bg-white border rounded-lg p-4
                hover:shadow-md transition cursor-pointer">
                <a href="?folder={{ folder.id }}" class="block">
                    <span class="text-gray-800 font-semibold
                        flex items-center space-x-2">
                        <span>📁</span>
                        <span>{{ folder.name }}</span>
                    </span>
                </a>
            </li>
        {% endfor %}

        <!-- Arquivos -->
        {% for file in files %}
            <li class="bg-white border rounded-lg p-4
                hover:shadow-md transition">
                <a href="{{ file.file.url }}" target="_blank"
                    class="block">
                    <span class="text-gray-800 font-semibold
                        flex items-center space-x-2">
                        <span>📄</span>
                        <span>{{ file.name }}</span>
                    </span>
                    <p class="text-xs text-gray-500">
                        Enviado em
                        {{ file.uploaded_at|date:"d/m/Y H:i" }}
                    </p>
                </a>
            </li>
        {% endfor %}
    </ul>
{% else %}
    <p class="pt-4 text-gray-500 italic">
        Nenhum item encontrado neste diretório.
    </p>
{% endif %}
```

![img](images/show-folders-and-files-01.png)  

> **Mas como nosso template conseguiu exibir as pastas e arquivos do usuário logado?**

**NOTE:**  
Isso tudo foi montado e nós passamos como contexto (context) no retorno da view (ação) `workspace_home()`:

```python
return render(request, "pages/workspace_home.html", context)
```

Continuando, agora vamos criar um tipo de navegação (breadcrumbs) para exibir o caminho hierárquico do usuário logado para que ele consiga voltar para a página anterior:

[workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<!-- 🧭 Breadcrumbs -->
<nav class="text-sm text-gray-600 my-4 flex items-center
    space-x-2">

    {% if current_folder %}

        {% if breadcrumbs|length > 1 %}
            {% with prev_folder=breadcrumbs|slice:"-2:-1"|first %}
                <a href="?folder={{ prev_folder.id }}"
                    class="text-blue-600 hover:underline
                        breadcrumb-drop"
                    data-folder-id="{{ prev_folder.id }}">
                    ← Voltar</a>
            {% endwith %}
        {% else %}
            <a href="{% url 'workspace_home' %}"
                class="text-blue-600 hover:underline
                    breadcrumb-drop"
                data-folder-id="">← Voltar à raiz</a>
        {% endif %}

        <span>/</span>

        <a href="{% url 'workspace_home' %}"
            class="hover:underline breadcrumb-drop"
            data-folder-id="">📁 Raiz</a>

        <span>/</span>

        {% for folder in breadcrumbs %}
            {% if not forloop.last %}
                <a href="?folder={{ folder.id }}"
                    class="hover:underline breadcrumb-drop"
                    data-folder-id="{{ folder.id }}">
                    {{ folder.name }}</a>
                <span>/</span>
            {% else %}
                <span class="font-semibold breadcrumb-drop"
                      data-folder-id="{{ folder.id }}">
                    {{ folder.name }}
                </span>
            {% endif %}
        {% endfor %}

    {% else %}
        <span class="text-gray-400 italic breadcrumb-drop"
              data-folder-id="">
            📁 Raiz
        </span>
    {% endif %}

</nav>
```

![img](images/breadcrumbs-01.png)









































































































---

<div id="refactor-folders-and-files-v1"></div>

## `Refatorando a exibição das pastas e arquivos (Clicks, Houver, Select, Escape, Click Outside)`

> Aqui nós vamos refatorar a exibição de pastas e arquivos porque algumas funcionalidades não estão funcionando corretamente.

Por exemplo, vamos atualizar para:

 - Quando alguém clicar 1 vez em um arquivo ou pasta seja apenas selecionado;
 - Quando alguém clicar 2 vezes em um arquivo ou pasta seja aberto;
 - Quando alguém aperta *ESC* a pasta ou arquivo selecionado deixe de ser selecionado;
 - Quando alguém aperta fora da pasta ou arquivo selecionado o mesmo deixa de ser selecionado.

> **Mas como fazer isso?**

Vamos começar entendo e atualizando o nosso template `workspace_home.html`:

[workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<!-- 📁 Listagem de pastas e arquivos -->
{% if folders or files %}
    <ul class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">


      ...


{% else %}
    <p class="pt-4 text-gray-500 italic">
        Nenhum item encontrado neste diretório.
    </p>
{% endif %}
```

Olhando para o código acima nós temos que:

 - `{% if folders or files %}`
   - Nós temos um `if` verificando se existe algum folder(s) ou file(s).
   - Se tiver nesse parte que nós vamos implementar algum mecanismo para exibir as pastas e arquivos.
 - `{% else %}`
   - Se não tiver nenhuma pasta (folders) ou arquivos (files) então vamos exibir uma mensagem dizendo que nenhuma pasta ou arquivo foi encontrada.

> **E agora como eu listo minhas pastas no bloco if**

```html
<ul class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">

    <!-- Pastas -->
    {% for folder in folders %}
        <li class="
                bg-white
                border
                rounded-lg
                p-4
                cursor-pointer
                transition
                transform
                hover:scale-102
                hover:bg-gray-200
                selectable-item"
            data-url="?folder={{ folder.id }}"
            data-target="_self"
            data-kind="folder"
            data-id="{{ folder.id }}"
            draggable="true">
                <div class="block">
                    <span class="text-gray-800
                                font-semibold flex
                                items-center space-x-2">
                        <span>📁</span>
                        <span>{{ folder.name }}</span>
                    </span>
                </div>
        </li>
    {% endfor %}

</ul>
```

 - **Primeiro veja que nós estamos criando uma lista:**
   - `<ul class="..."></ul>`
 - **Depois vejam nós estamos criando os itens da lista dinamicamente:**
   - `{% for folder in folders %}`
     - `<li class="..."></li>`

> **E os atributos desta lista?**

```html
<li class="
        bg-white
        border
        rounded-lg
        p-4
        cursor-pointer
        transition
        transform
        hover:scale-102
        hover:bg-gray-200
        selectable-item"
    data-url="?folder={{ folder.id }}"
    data-target="_self"
    data-kind="folder"
    data-id="{{ folder.id }}"
    draggable="true">
```

 - `bg-white`
   - Define a cor de fundo como branco (Tailwind).
 - `border`
   - Adiciona uma borda padrão (1px sólida).
   - Cor padrão: border-gray-200.
 - `rounded-lg`
   - Arredonda os cantos do elemento.
   - lg = tamanho grande do raio.
 - `p-4`
   - Adiciona padding interno.
   - 4 = escala do Tailwind (1rem / 16px)
 - `cursor-pointer`
   - Muda o cursor do mouse para a “mãozinha”.
   - Indica que o item é clicável.
 - `transition`
   - Ativa transições suaves para propriedades animáveis.
   - Normalmente usada junto com `hover:*`
 - `transform`
   - Habilita transformações CSS.
   - Obrigatório para: `hover:scale-105`
   - Sem isso, o scale não funciona corretamente.
 - `hover:scale-102`
   - Aumenta o item 2% ao passar o mouse.
   - Dá sensação de “card elevando”.
 - `hover:bg-gray-200`
   - Muda o fundo no hover.
 - `selectable-item`
   - 📌 Classe customizada (sua ou do projeto).
   - ❗ Não existe no Tailwind por padrão.
   - Exemplo típico de uso: `document.querySelectorAll('.selectable-item')`
 - `data-url="?folder={{ folder.id }}"`
   - Guarda a URL da pasta (atual).
   - Usado pelo JS para abrir o arquivo.
   - Exemplo: `const url = item.dataset.url;`
 - `data-target="_self"`
   - Diz ao JS para abrir em nova aba.
   - Exemplo: `window.open(url, "_blank");`
 - `data-kind="folder"`
   - Define o tipo do item.
   - Pode ser:
     - file.
     - folder.
 - `data-id="{{ folder.id }}"`
   - ID do arquivo no backend (Django).
   - Usado para:
     - seleção.
     - drag & drop.
     - ações (delete, rename).
 - `draggable="true"`
   - Habilita drag and drop.
   - HTML puro (não é Tailwind).
   - 📌 Permite arrastar arquivos/pastas

> **E agora como eu listo meus arquivos no bloco if**

A lógica é a mesma, porém, para listar os arquivos:

```html
<ul class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">

<!-- Arquivos -->
{% for file in files %}
    <li class="
            bg-white
            border
            rounded-lg
            p-4
            cursor-pointer
            transition
            transform
            hover:scale-102
            hover:bg-gray-200
            selectable-item"
        data-url="{{ file.file.url }}"
        data-target="_blank"
        data-kind="file" data-id="{{ file.id }}"
        draggable="true">
            <div class="block">
                <span class="
                            text-gray-800
                            font-semibold
                            flex items-center
                            space-x-2">
                    <span>📄</span>
                    <span>{{ file.name }}</span>
                </span>
            </div>
    </li>
{% endfor %}

</ul>
```

Porém, agora nós temos a seguinte situação, quando nós passamos o mouse em cima de alguma pasta ou arquivo:

 - Ele aumenta 2% (hover:scale-102).
 - Muda o fundo (hover:bg-gray-200).
 - **NOTE:** Porém, eu não abrir ou selecionar nenhum deles ainda.

Para resolver isso vamos criar o `workspace_home.js`:

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
(function () {

    'use strict';

})(); // IIFE
```

De início nós temos a seguinte implementação:

 - `(function () { ... })();`
   - IIFE (Immediately Invoked Function Expression).
   - Isso é uma função autoexecutável.
   - **O que significa?**
     - A função é criada;
     - E executada imediatamente;
     - Sem precisar chamar pelo nome.
 - `'use strict';`
   - Ativa o modo estrito do JavaScript.
   - Ele torna o JavaScript mais rigoroso e seguro.
   - Exemplo: `x = 10; // cria variável global sem querer`

Agora, vamos continuar com a implementação:

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
(function () {

    'use strict';

    // Aguarda o carregamento completo do DOM
    document.addEventListener("DOMContentLoaded", function () {
    
    }); // DOMContentLoaded

})(); // IIFE
```

 - `document.addEventListener("DOMContentLoaded", function () { ... })`
   - **Esse trecho é um dos mais importantes do JavaScript em páginas HTML.**
   - `document`
     - Representa toda a página HTML.
     - É o objeto principal do DOM (Document Object Model).
     - Tudo que você faz com HTML via JS começa aqui:
       - `document.querySelector(...)`
       - `document.getElementById(...)`
   - `addEventListener(...)`
     - Método que escuta eventos.
     - Diz ao navegador:
       - “Quando isso acontecer, execute essa função”
       - Sintaxe geral:
         - `element.addEventListener(evento, callback);`
   - `"DOMContentLoaded"`
     - *O que é esse evento?*
     - É um evento que dispara quando o HTML foi totalmente carregado e interpretado.
     - ⚠️ Importante:
       - Não espera imagens;
       - Não espera vídeos;
       - Não espera fontes externas.
     - Só espera:
       - ✔ HTML;
       - ✔ estrutura do DOM pronta.
   - `function () { ... }`
     - Callback (função de retorno).
     - Essa função não executa imediatamente.
     - Ela fica registrada.
     - Só roda quando o evento acontece.
     - 📌 Em português:
       - *“Quando o DOM estiver pronto, execute isso aqui”*

Bem, até então só implementamos a estrutura da função IIFE, agora vamos implementar a lógica para satisfazer os objetivos desta seção:

 - Quando alguém clicar 1 vez em um arquivo ou pasta seja apenas selecionado;
 - Quando alguém clicar 2 vezes em um arquivo ou pasta seja aberto;
 - Quando alguém aperta *ESC* a pasta ou arquivo selecionado deixe de ser selecionado;
 - Quando alguém aperta fora da pasta ou arquivo selecionado o mesmo deixa de ser selecionado.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
(function () {

    'use strict';

    // Aguarda o carregamento completo do DOM
    document.addEventListener("DOMContentLoaded", function () {
    
        // Seleciona todos os itens clicáveis
        const items = document.querySelectorAll(".selectable-item");
        let selectedItem = null;

        /**
         * Remove seleção de todos os itens
         */
        function clearSelection() {
            items.forEach(item => {
                item.classList.remove("ring-2", "ring-blue-500");
            });
            selectedItem = null;
        }

        /**
         * Seleciona visualmente um item
         */
        function selectItem(item) {
            clearSelection();
            item.classList.add("ring-2", "ring-blue-500");
            selectedItem = item;
        }

        // Aplica eventos a cada item
        items.forEach(item => {

            // Clique simples → seleciona
            item.addEventListener("click", function (event) {
                event.preventDefault();
                selectItem(item);
            });

            // Duplo clique → navega
            item.addEventListener("dblclick", function () {
                const url = item.dataset.url;
                const target = item.dataset.target || "_self";

                if (!url) return;

                if (target === "_blank") {
                    window.open(url, "_blank");
                } else {
                    window.location.href = url;
                }
            });

        }); // items.forEach

        // Clique fora → limpa seleção
        document.addEventListener("click", function (event) {
            const clickedItem = event.target.closest(".selectable-item");
            if (!clickedItem) {
                clearSelection();
            }
        });

        // Limpa seleção ao pressionar ESC
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                clearSelection();
            }
        });

    }); // DOMContentLoaded
})(); // IIFE
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```js
const items = document.querySelectorAll(".selectable-item");
let selectedItem = null;
```

 - `items`
   - Guarda todos os itens do workspace que podem ser selecionados (pastas e arquivos).
   - **const por que?**
     - a lista não muda.
     - os itens continuam os mesmos.
 - `selectedItem`
   - Guarda qual item está selecionado no momento.
   - **let por que?**
     - let → valor pode mudar.
     - começa como null → nenhum item selecionado.
     - Depois: selectedItem = itemClicado;
 - **Instrução por instrução:**
   - `document` → página HTML.
   - `querySelectorAll` → busca vários elementos.
   - `".selectable-item"` → classe usada nos `<li>`.

**Função clearSelection:**
```js
/**
 * Remove seleção de todos os itens
 */
function clearSelection() {
    items.forEach(item => {
        item.classList.remove("ring-2", "ring-blue-500");
    });
    selectedItem = null;
}
```

 - **Para que serve?**
   - Remove a seleção visual de todos os itens.
   - Reseta o estado interno de seleção.
 - `items.forEach(item => {}`
   - Percorre cada item do workspace.
   - item = um `<li>` por vez.
 - `item.classList.remove("ring-2", "ring-blue-500");`
   - Remove classes Tailwind que indicam seleção.
   - Essas classes criam o “contorno azul”.
   - Visualmente:
     - antes → item selecionado;
     - depois → item normal.
 - `selectedItem = null;`
   - Nenhum item está selecionado.
   - Estado interno limpo.
   - Muito importante para:
     - evitar conflito de seleção.
     - saber se algo está selecionado ou não.

**Função selectItem:**
```js
/**
 * Seleciona visualmente um item
 */
function selectItem(item) {
    clearSelection();
    item.classList.add("ring-2", "ring-blue-500");
    selectedItem = item;
}
```

 - **Para que serve?**
   - Seleciona um único item.
   - Garante que só um fique selecionado por vez.
 - `clearSelection();`
   - Remove qualquer seleção anterior.
   - Evita múltiplos itens selecionados.
   - Comportamento de explorador de arquivos real.
 - `item.classList.add("ring-2", "ring-blue-500");`
   - Adiciona borda azul ao item.
   - Feedback visual claro.
 - `selectedItem = item;`
   - Guarda o item selecionado.
   - Permite ações futuras:
     - delete;
     - rename;
     - move;
     - abrir.

**Aplica eventos a cada item:**
```js
items.forEach(item => {});
```

 - **Para que serve?**
   - Percorre cada item do workspace.
   - Permite adicionar eventos em todos.
 - **Sem isso:**
   - só um item teria comportamento.
   - os outros não responderiam.

**Clique simples → seleciona:**
```js
item.addEventListener("click", function (event) {
    event.preventDefault();
    selectItem(item);
});
```

 - **Para que serve?**
   - Selecionar o item com clique simples.
 - `item.addEventListener("click", function (event) {...})`
   - Escuta o clique do mouse.
   - *event* = informações do clique.
 - `event.preventDefault();`
   - Evita comportamento padrão.
   - Importante se:
     - `houver <a>`;
     - `houver drag`;
     - houver navegação automática.
 - `selectItem(item);`
   - Marca visualmente o item.
   - Atualiza *"selectedItem"*.
   - Igual ao Windows / macOS:
     - 1 clique → seleciona.
     - não abre.

**Duplo clique → navega:**
```js
item.addEventListener("dblclick", function () {
    const url = item.dataset.url;
    const target = item.dataset.target || "_self";

    if (!url) return;

    if (target === "_blank") {
        window.open(url, "_blank");
    } else {
        window.location.href = url;
    }
});
```

 - **Para que serve?**
   - Abrir arquivo ou pasta com duplo clique.

**Clique fora → limpa seleção:**
```js
document.addEventListener("click", function (event) {
    const clickedItem = event.target.closest(".selectable-item");
    if (!clickedItem) {
        clearSelection();
    }
});
```

 - **Para que serve?**
   - Clicou fora dos itens → desseleciona tudo.

**ESC → limpa seleção:**
```js
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        clearSelection();
    }
});
```

 - **Para que serve?**
   - Pressionar ESC remove a seleção.









































































































---

<div id="add-buttons-new-folder"></div>

## `Adicionando o botão (➕ Nova Pasta)`

> Aqui nós vamos implementar um botão (➕ Nova Pasta) que vai abrir o modal de criação de pastas.

Vamos começar adicionando uma `<div>` que vai armazenar esse botão:

[workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<!-- 📌 Botões -->
<div class="mb-6 flex items-center gap-3 flex-wrap" data-preserve-selection="true">

</div>
```

Agora vamos adicionar o botão de **criação de pasta** e sua lógica:

[workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<button
    command="show-modal"
    commandfor="create_folder_modal"
    class="inline-block
            bg-green-600
            hover:bg-green-700
            text-white
            px-4
            py-2
            rounded">
    ➕ Nova Pasta
</button>
```

 - **Para que serve esse botão?**
   - Esse botão abre o modal de criação de pasta (create_folder_modal).
   - Ele não cria a pasta diretamente.
   - Ele apenas:
     - Interrompe o comportamento padrão;
     - Abre o `<dialog>` de criação;
     - Dá foco no campo de nome da pasta.
 - `command="show-modal"`
   - 📌 Não é um atributo HTML padrão.
   - Ele existe exclusivamente para o JavaScript identificar esse botão.
   - No seu [workspace_home.js](../static/workspace/js/workspace_home.js) ele tem essa lógica:
     - `const openCreateBtn = document.querySelector(`
       - `'button[command="show-modal"]' +`
       - `'[commandfor="create_folder_modal"]'`
     - `);`
   - 💡 Ou seja:
     - O JS procura exatamente por um botão com:
       - `command="show-modal"`
       - `commandfor="create_folder_modal"`
       - Esse atributo funciona como um identificador semântico:
         - *“Esse botão serve para abrir um modal”*  
 - `commandfor="create_folder_modal"`
   - 📌 Diz qual modal deve ser aberto.
   - Ele aponta para: `<dialog id="create_folder_modal">`
   - No JS: `modal.showModal();`
   - 👉 O JS sabe qual modal abrir porque:
     - Ele já capturou o modal pelo id;
     - Esse atributo deixa claro o vínculo botão ↔ modal.
   - 💡 Isso facilita:
     - Reutilizar lógica;
     - Criar outros botões para outros modais no futuro.

> **Mas onde está esse modal?**

Vamos implementar ele agora:

[workspace/templates/modals/create_folder_modal.html](../workspace/templates/modals/create_folder_modal.html)
```html
<!-- MODAL Criar Pasta -->
<el-dialog>
    <dialog
        id="create_folder_modal"
        aria-labelledby="modal-title"
        {% if show_modal %}data-auto-open="true"{% endif %}
        class="
            fixed
            inset-0
            size-auto
            max-h-none
            max-w-none
            overflow-y-auto
            bg-transparent
            backdrop:bg-transparent">

        <el-dialog-backdrop
            class="
                fixed
                inset-0
                bg-gray-900/50
                transition-opacity">
        </el-dialog-backdrop>

        <div
            tabindex="0"
            class="
                flex
                min-h-full
                items-center
                justify-center
                p-4
                text-center
                sm:p-0">
            <el-dialog-panel
                class="
                    relative
                    transform
                    rounded-lg
                    bg-white
                    shadow-xl
                    transition-all
                    sm:w-full
                    sm:max-w-md
                    p-6">
                <form method="post" action="">
                    {% csrf_token %}
                    <input 
                        type="hidden" 
                        name="next" 
                        value="{{ request.get_full_path }}">
                    <input
                        type="hidden" 
                        name="parent" 
                        value="{{ current_folder.id|default_if_none:'' }}">

                    <h3 id="modal-title" class="text-lg font-semibold text-gray-900 mb-4">
                        Criar nova pasta
                    </h3>

                    <div>
                        <label
                            for="folder_name"
                            class="
                                block
                                text-sm
                                font-medium
                                text-gray-700">
                            Nome da pasta
                        </label>
                        <input
                            type="text"
                            name="name"
                            id="folder_name"
                            required
                            class="
                                mt-1 block
                                w-full
                                px-4
                                py-2
                                border
                                rounded-lg"
                            autocomplete="off"
                            value="{{ form.name.value|default:'' }}">

                        {% if form.name.errors %}
                            <p id="server-error" class="text-sm text-red-500 mt-1">
                                {{ form.name.errors.0 }}
                            </p>
                        {% else %}
                            <p id="server-error" class="text-sm text-red-500 mt-1 hidden"></p>
                        {% endif %}
                    </div>

                    <div class="mt-6 flex justify-end space-x-2">

                        <button
                            type="submit"
                            id="create_folder_btn"
                            class="
                                px-4
                                py-2
                                bg-green-600
                                hover:bg-green-700
                                text-white
                                rounded">
                            Criar
                        </button>

                        <button
                            type="button"
                            command="close"
                            commandfor="create_folder_modal"
                            class="
                                px-4
                                py-2
                                bg-gray-200
                                hover:bg-gray-300
                                rounded">
                            Cancelar
                        </button>
                    </div>
                </form>
            </el-dialog-panel>
        </div>
    </dialog>

</el-dialog> <!-- MODAL Criar Pasta -->
```

Como esse *modal* é muito grande vamos explicar apenas as partes cruciais:

**Atributos importantes:**
```html
<!-- MODAL Criar Pasta -->
<el-dialog>
    <dialog
        id="create_folder_modal"
        aria-labelledby="modal-title"
        {% if show_modal %}data-auto-open="true"{% endif %}
        class="
            fixed
            inset-0
            size-auto
            max-h-none
            max-w-none
            overflow-y-auto
            bg-transparent
            backdrop:bg-transparent">
    </dialog>
</el-dialog>
```

### `✅ Quando o id="create_folder_modal" é utilizado?`

Esse **id** é fundamental e é usado em 3 lugares diferentes:

**1️⃣ No JavaScript (abrir o modal):** [static/workspace/js/workspace_home.js](../static/workspace/js/workspace_home.js)
```js
const modal = document.querySelector("#create_folder_modal");
```

**2️⃣ No botão “Nova Pasta”:** [workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<button
    command="show-modal"
    commandfor="create_folder_modal">
    Nova Pasta
</button>
```

```
Botão → create_folder_modal → dialog
```

**3️⃣ No botão “Cancelar”:** [workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<button
    command="close"
    commandfor="create_folder_modal">
    Cancelar
</button>
```

> **NOTE:**  
> O JS usa esse mesmo ID para fechar o modal correto.

**Campos value dos inputs:**
```html
<form method="post" action="">
    {% csrf_token %}
    <input 
        type="hidden" 
        name="next" 
        value="{{ request.get_full_path }}"
    >
    <input
        type="hidden" 
        name="parent" 
        value="{{ current_folder.id|default_if_none:'' }}"
    >
</form>
```

 - `value="{{ request.get_full_path }}"`
   - É a URL atual completa, por exemplo: `/workspace?folder=12`
   - **Para que serve?**
     - Após criar a pasta, o backend faz:
       - `return redirect(request.POST.get("next", "workspace_home"))`
   - 👉 Resultado:
     - Usuário volta exatamente para a pasta onde estava;
     - Mantém breadcrumbs e navegação.
   - 🧠 Sem isso:
     - Você sempre voltaria para a raiz;
     - UX ruim.
 - `value="{{ current_folder.id|default_if_none:'' }}"`
   - **O que isso faz?**
     - Se o usuário estiver dentro de uma pasta, envia o ID dela;
     - Se estiver na raiz, envia vazio ("").
     - Exemplos:
       - `value="15"   <!-- dentro da pasta 15 -->`
       - `value=""     <!-- raiz -->`

> **Mas como eu realmente crio uma nova pasta?**

Bem, nós precisamos implementar uma view (ação) para isso, mas antes vamos criar uma ROTA/URL para isso:

[workspace/urls.py](../workspace/urls.py)
```python
from django.urls import path

from . import views

urlpatterns = [
    path(
        route="workspace/",
        view=views.workspace_home,
        name="workspace_home"
    ),
    path(
        route="create-folder/",
        view=views.create_folder,
        name="create_folder"
    ),
]
```

Agora nós precisamos de uma view (ação) para criar uma nova pasta, mas antes vamos criar uma função utilitária `build_breadcrumbs()`:

[workspace/views.py](../workspace/views.py)
```python
def build_breadcrumbs(folder):
    breadcrumbs = []
    while folder:
        breadcrumbs.insert(0, folder)
        folder = folder.parent
    return breadcrumbs
```

A função `build_breadcrumbs()` serve para montar o caminho completo de navegação (breadcrumbs) de uma pasta dentro do workspace.

Em termos práticos, ela:

 - Recebe uma pasta atual;
 - Sobe pela hierarquia de pastas usando o campo parent;
 - Constrói uma lista ordenada da raiz até a pasta atual;
 - Retorna essa lista para ser usada no template HTML.

Esse resultado é usado para exibir algo como:

```bash
Raiz / Projetos / Django / Workspace
```

 - 📌 Essa função não acessa o banco diretamente;
 - 📌 Ela trabalha apenas com os objetos Folder já carregados;
 - 📌 É uma função utilitária, simples e eficiente.

Ótimo, agora com a função utilitária pronta, vamos criar uma view (ação) para criar uma nova pasta:

[workspace/views.py](../workspace/views.py)
```python
from .forms import FolderForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render


@login_required(login_url="/")
def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)

        parent_id = request.POST.get("parent")
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(
                Folder,
                id=parent_id,
                owner=request.user
            )

        if form.is_valid():
            name = form.cleaned_data["name"]

            if Folder.objects.filter(
                owner=request.user,
                name__iexact=name,
                parent=parent_folder,
                is_deleted=False
            ).exists():
                form.add_error(
                    "name",
                    "Já existe uma pasta com esse nome nesse diretório."
                )
            else:
                new_folder = form.save(commit=False)
                new_folder.owner = request.user
                new_folder.parent = parent_folder
                new_folder.save()

                messages.success(
                    request,
                    f"Pasta '{name}' criada com sucesso!"
                )
                return redirect(
                    request.POST.get("next", "workspace_home")
                )

        if parent_folder:
            folders = Folder.objects.filter(
                parent=parent_folder,
                is_deleted=False
            )
            files = File.objects.filter(
                folder=parent_folder,
                is_deleted=False
            )
            breadcrumbs = build_breadcrumbs(parent_folder)
        else:
            folders = Folder.objects.filter(
                owner=request.user,
                parent__isnull=True,
                is_deleted=False
            )
            files = File.objects.filter(
                uploader=request.user,
                folder__isnull=True,
                is_deleted=False
            )
            breadcrumbs = []

        context = {
            "form": form,
            "current_folder": parent_folder,
            "folders": folders,
            "files": files,
            "breadcrumbs": breadcrumbs,
            "show_modal": True,
        }

        return render(request, "pages/workspace_home.html", context)

    return redirect("workspace_home")
```

> **E agora é só criar uma nova pasta a partir do modal?**

Não, antes nós precisamos referenciar a ROTA/URL que nós criamos com o formulário dentro do modal:

[workspace/templates/pages/workspace_home.html](../workspace/templates/pages/workspace_home.html)
```html
<form method="post" action="{% url 'create_folder' %}">
    {% csrf_token %}

</form>
```

Ótimo, estamos conseguindo criar uma nova pasta e salvando no Banco de Dados.



















































---

<div id="refatoring-modal-to-select-input"></div>

## `Refatorando o modal para abrir selecionando o campo de digitação`

> Bem, nós precisamos refatorar o modal para assim que abrir selecionar o campo de digitação automaticamente.

Vamos começar adicionando o seguinte código:

[static/workspace/js/workspace_home.js](../static/workspace/js/workspace_home.js)
```js
// Usa delegação de eventos para capturar cliques em
// elementos com atributo "command"
document.addEventListener("click", function (event) {
    // Verifica se o elemento clicado (ou seu pai) tem
    // o atributo "command"
    const commandElement = event.target.closest(
        '[command]'
    );
    
    // Se não encontrou, ignora o evento
    if (!commandElement) return;
    
    // Obtém o tipo de comando (ex: "show-modal", "close")
    const command = commandElement.getAttribute("command");
    
    // Obtém o alvo do comando (ex: "create_folder_modal")
    const commandFor = commandElement.getAttribute(
        "commandfor"
    );
    
    // Se não há comando ou alvo, ignora
    if (!command || !commandFor) return;
    
    // ========================================================
    // COMANDO: show-modal
    // ========================================================
    // Abre um modal e foca no campo de input
    if (command === "show-modal") {
        // Busca o elemento <dialog> pelo ID especificado
        const modal = document.getElementById(commandFor);
        
        // Se o modal não existe, não faz nada
        if (!modal) return;
        
        // Abre o modal usando a API nativa do HTML5
        modal.showModal();
        
        // Busca o campo de input dentro do modal
        // Usa o ID "folder_name" que está no HTML
        const inputField = modal.querySelector(
            "#folder_name"
        );
        
        // Se o campo existe, foca nele
        // O setTimeout garante que o foco aconteça após
        // o modal estar totalmente renderizado
        if (inputField) {
            setTimeout(function () {
                inputField.focus();
                // Seleciona todo o texto (se houver)
                // para facilitar substituição
                inputField.select();
            }, 100);
        }
    }
    
    // ========================================================
    // COMANDO: close
    // ========================================================
    // Fecha um modal
    if (command === "close") {
        // Busca o elemento <dialog> pelo ID especificado
        const modal = document.getElementById(commandFor);
        
        // Se o modal não existe, não faz nada
        if (!modal) return;
        
        // Fecha o modal usando a API nativa do HTML5
        modal.close();
    }
});
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):


**Delegação de eventos:**
```js
document.addEventListener("click", function (event) {
    const commandElement = event.target.closest('[command]');
    ...
});
```

 - Usa delegação para capturar cliques em elementos com `command`.
 - Funciona mesmo se o botão for adicionado dinamicamente.

**Identificação do comando:**
```js
const command = commandElement.getAttribute("command");
const commandFor = commandElement.getAttribute("commandfor");
```

 - Lê os atributos para determinar a ação e o alvo.

**Abertura do modal:**
```js
if (command === "show-modal") {
    const modal = document.getElementById(commandFor);
    if (!modal) return;
    modal.showModal();
    ...
}
```

 - Localiza o modal pelo ID e abre com `showModal()`.

**Foco no campo de digitação:**
```js
const inputField = modal.querySelector("#folder_name");
if (inputField) {
    setTimeout(function () {
        inputField.focus();
        inputField.select();
    }, 100);
}
```

 - Localiza o `<input>` dentro do modal.
 - Usa `setTimeout()` para garantir que o foco ocorra após a renderização.
 - `focus()` foca o campo; `select()` seleciona o texto existente.

**Fechamento do modal:**
```js
if (command === "close") {
    const modal = document.getElementById(commandFor);
    if (!modal) return;
    modal.close();
}
```

 - Fecha o modal quando o botão *"Cancelar"* é clicado.

**Verificação do HTML (opcional):**
```html
<!-- Linha 228-241 -->
<input
    type="text"
    name="name"
    id="folder_name"  <!-- ✅ ID único e correto -->
    required
    class="
        mt-1 block
        w-full
        px-4
        py-2
        border
        rounded-lg"
    autocomplete="off"
    value="{{ form.name.value|default:'' }}">


<!-- Linha 160-161 -->
<dialog
    id="create_folder_modal"  <!-- ✅ ID correto -->
    aria-labelledby="modal-title"
    ...
```



















































---

<div id="refatoring-to-exists-folder-name"></div>

## `Refatorando para quando o usuário digitar um nome para uma pasta existente`

Continuando nas refatorações, nós temos o seguinte problema:

 - Quando um usuário digita o nome de uma pasta que já existe essa pasta não é criada, porém, o fecha.
 - Quando eu clico novamente em "➕ Nova Pasta" ele continua com o mesmo nome que eu digitei e a mensagem:
   - Já existe uma pasta com esse nome nesse diretório.

> **O que nós queremos agora?**

Eu quero que quando eu digitar um nome de ums pasta que já exista:

 - Apareça a mensagem de erro imediatamente: *"Já existe uma pasta com esse nome nesse diretório."*;
 - Se eu clicar em cancelar limpe a frase/palavra que eu digitei no campo;
 - Limpe a mensagem de erro: *"Já existe uma pasta com esse nome nesse diretório."*;
 - **NOTE:** Como se fosse uma nova sessão de criação de pasta.

Vamos começar implementando a função `getExistingFolderNames()` responsável por descobrir quais pastas já existem no diretório atual, diretamente a partir do HTML renderizado na página.

> Ela não consulta o backend, nem faz requisições HTTP.

Em vez disso, ela:

 - Varre o DOM;
 - Identifica todos os itens que representam pastas;
 - Extrai o nome visível de cada pasta;
 - Normaliza esses nomes (minúsculas);
 - Retorna uma lista pronta para comparação

Essa função é a base da validação de nome duplicado, sendo usada por:

 - folderNameExists (Função que vamos criar ainda);
 - Validação em tempo real (evento input);
 - Bloqueio da submissão do formulário;

Ela garante que o usuário não crie uma pasta com nome repetido no mesmo nível:

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
function getExistingFolderNames() {
    const folderItems = document.querySelectorAll(
        '[data-kind="folder"]'
    );
    const folderNames = [];
    
    folderItems.forEach(function (item) {
        // O nome da pasta está no segundo span dentro do item
        // Estrutura: <span><span>📁</span><span>Nome</span></span>
        // Busca todos os spans aninhados
        const allSpans = item.querySelectorAll("span span");
        
        if (allSpans.length >= 2) {
            // Pega o último span que contém o nome da pasta
            const nameSpan = allSpans[allSpans.length - 1];
            const folderName = nameSpan.textContent.trim();
            
            // Normaliza o nome para comparação (minúsculas)
            if (folderName) {
                const normalized = folderName.toLowerCase();
                folderNames.push(normalized);
            }
        }
    });
    
    return folderNames;
}
```

Agora, vamos implementar a função `folderNameExists(folderName)` que vai ser um validador lógico, simples e reutilizável.

O papel dela é responder apenas uma pergunta:

> “Já existe uma pasta com esse nome neste diretório?”

Para isso, ela:

 - Normaliza o nome digitado pelo usuário;
 - Obtém a lista de nomes existentes via `getExistingFolderNames()`;
 - Compara os valores de forma segura (case-insensitive);

Ela centraliza a regra de negócio da validação, evitando:

 - Código duplicado;
 - Lógicas espalhadas pelo JS;
 - Erros de comparação (maiúsculas/minúsculas).

Essa função é usada em:

 - Validação enquanto o usuário digita;
 - Validação antes do envio do formulário.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
function folderNameExists(folderName) {
    if (!folderName || !folderName.trim()) {
        return false;
    }
    
    const existingNames = getExistingFolderNames();
    const normalizedName = folderName.trim().toLowerCase();
    
    return existingNames.includes(normalizedName);
}
```

Continuando, vamos implementar a função `showErrorMessage(errorElement, message)` responsável por exibir mensagens de erro no modal, de forma padronizada.

Ela abstrai completamente a lógica de:

 - Inserir texto de erro;
 - Tornar a mensagem visível;
 - Garantir consistência visual.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
function showErrorMessage(errorElement, message) {
    if (!errorElement) return;
    
    errorElement.textContent = message;
    errorElement.classList.remove("hidden");
}
```

Agora, vamos implementar a função `hideErrorMessage(errorElement)` que é um complemento direto de `showErrorMessage()`.

O papel dela é:

 - Limpar o texto de erro;
 - Ocultar visualmente a mensagem;
 - Restaurar o estado “limpo” do modal

Ela é chamada quando:

 - O campo fica vazio;
 - O nome digitado passa a ser válido;
 - O modal é aberto novamente;
 - O modal é cancelado.

Essa separação (show/hide) deixa o fluxo de validação:

 - Mais legível;
 - Mais previsível;
 - Mais fácil de evoluir futuramente.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
function hideErrorMessage(errorElement) {
    if (!errorElement) return;
    
    errorElement.textContent = "";
    errorElement.classList.add("hidden");
}
```

Agora, vamos implementar a função `initializeFolderValidation()`, essa é a função mais importante de todo o sistema de validação do modal.

Ela é responsável por configurar e garantir que:

 - A validação em tempo real esteja ativa;
 - O formulário não seja enviado com nome inválido;
 - Os listeners não sejam duplicados;
 - O comportamento funcione mesmo quando o modal abre dinamicamente.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
// Referência ao modal de criação de pasta
const createFolderModal = document.getElementById(
    "create_folder_modal"
);

function initializeFolderValidation() {
    if (!createFolderModal) return;
    
    const folderNameInput = createFolderModal.querySelector(
        "#folder_name"
    );
    const errorMessage = createFolderModal.querySelector(
        "#server-error"
    );
    const createFolderForm = createFolderModal.querySelector(
        "form"
    );
    
    if (!folderNameInput || !errorMessage) return;
    
    // Remove listeners anteriores se existirem (usando clone)
    // para evitar duplicação
    const hasInputListener = folderNameInput.hasAttribute(
        "data-validation-attached"
    );
    
    if (!hasInputListener) {
        // Validação em tempo real enquanto o usuário digita
        folderNameInput.addEventListener("input", function () {
            const folderName = this.value.trim();
            
            // Se o campo estiver vazio, remove o erro
            if (!folderName) {
                hideErrorMessage(errorMessage);
                return;
            }
            
            // Verifica se o nome já existe
            if (folderNameExists(folderName)) {
                showErrorMessage(
                    errorMessage,
                    "Já existe uma pasta com esse nome " +
                    "nesse diretório."
                );
            } else {
                hideErrorMessage(errorMessage);
            }
        });
        
        folderNameInput.setAttribute(
            "data-validation-attached",
            "true"
        );
    }
    
    // Previne submissão do formulário se houver erro
    if (createFolderForm && 
        !createFolderForm.hasAttribute("data-submit-listener")) {
        createFolderForm.addEventListener("submit", function (
            event
        ) {
            const folderName = folderNameInput.value.trim();
            
            // Se o campo estiver vazio, permite validação
            // HTML5 padrão
            if (!folderName) {
                return;
            }
            
            // Se o nome já existe, previne a submissão
            if (folderNameExists(folderName)) {
                event.preventDefault();
                showErrorMessage(
                    errorMessage,
                    "Já existe uma pasta com esse nome " +
                    "nesse diretório."
                );
                // Foca no campo para facilitar correção
                folderNameInput.focus();
                folderNameInput.select();
            }
        });
        
        createFolderForm.setAttribute(
            "data-submit-listener",
            "true"
        );
    }
}
```

Agora vamos atualizar o `document.addEventListener("click", function (event)`:

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
// Usa delegação de eventos para capturar cliques em
// elementos com atributo "command"
document.addEventListener("click", function (event) {
    // Verifica se o elemento clicado (ou seu pai) tem
    // o atributo "command"
    const commandElement = event.target.closest(
        '[command]'
    );
    
    // Se não encontrou, ignora o evento
    if (!commandElement) return;
    
    // Obtém o tipo de comando (ex: "show-modal", "close")
    const command = commandElement.getAttribute("command");
    
    // Obtém o alvo do comando (ex: "create_folder_modal")
    const commandFor = commandElement.getAttribute(
        "commandfor"
    );
    
    // Se não há comando ou alvo, ignora
    if (!command || !commandFor) return;
    
    // ========================================================
    // COMANDO: show-modal
    // ========================================================
    // Abre um modal e foca no campo de input
    if (command === "show-modal") {
        // Busca o elemento <dialog> pelo ID especificado
        const modal = document.getElementById(commandFor);
        
        // Se o modal não existe, não faz nada
        if (!modal) return;
        
        // Limpa o campo e mensagem de erro ao abrir o modal
        if (commandFor === "create_folder_modal") {
            const inputField = modal.querySelector(
                "#folder_name"
            );
            const errorMessage = modal.querySelector(
                "#server-error"
            );
            
            if (inputField) {
                inputField.value = "";
                // Dispara evento input para garantir validação
                inputField.dispatchEvent(new Event("input", {
                    bubbles: true
                }));
            }
            if (errorMessage) {
                errorMessage.textContent = "";
                errorMessage.classList.add("hidden");
            }
            
            // Garante que a validação está inicializada
            setTimeout(initializeFolderValidation, 50);
        }
        
        // Abre o modal usando a API nativa do HTML5
        modal.showModal();
        
        // Busca o campo de input dentro do modal
        // Usa o ID "folder_name" que está no HTML
        const inputField = modal.querySelector(
            "#folder_name"
        );
        
        // Se o campo existe, foca nele
        // O setTimeout garante que o foco aconteça após
        // o modal estar totalmente renderizado
        if (inputField) {
            setTimeout(function () {
                inputField.focus();
                // Seleciona todo o texto (se houver)
                // para facilitar substituição
                inputField.select();
            }, 100);
        }
    }
    
    // ========================================================
    // COMANDO: close
    // ========================================================
    // Fecha um modal
    if (command === "close") {
        // Busca o elemento <dialog> pelo ID especificado
        const modal = document.getElementById(commandFor);
        
        // Se o modal não existe, não faz nada
        if (!modal) return;
        
        // Limpa o campo e mensagem de erro ao cancelar
        if (commandFor === "create_folder_modal") {
            const inputField = modal.querySelector(
                "#folder_name"
            );
            const errorMessage = modal.querySelector(
                "#server-error"
            );
            
            if (inputField) {
                inputField.value = "";
            }
            if (errorMessage) {
                errorMessage.textContent = "";
                errorMessage.classList.add("hidden");
            }
        }
        
        // Fecha o modal usando a API nativa do HTML5
        modal.close();
    }
});
```

Por fim, vamos criar um `bloco if` que vai ser responsável por orquestrador final da validação, o objetivo dele vai ser garantir que:

 - O DOM esteja completamente carregado;
 - O modal exista na página;
 - A validação seja inicializada no momento certo;
 - O comportamento funcione mesmo em cenários especiais.

[workspace_home.js](../static/workspace/js/workspace_home.js)
```js
// Inicializa a validação quando o DOM estiver pronto
if (createFolderModal) {
    // Aguarda um pouco para garantir que o DOM está completo
    setTimeout(function () {
        initializeFolderValidation();
        
        // Se o modal abre automaticamente (erro do servidor),
        // garante que a validação esteja ativa
        if (createFolderModal.hasAttribute("data-auto-open")) {
            // Abre o modal automaticamente
            createFolderModal.showModal();
            
            // Aguarda o modal abrir completamente
            setTimeout(function () {
                initializeFolderValidation();
            }, 300);
        }
    }, 100);
}
```

---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
