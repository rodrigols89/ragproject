# RAG Project

 - [**Introdução e Objetivos do Projeto**](#intro-to-the-project)
 - **Estrutura do Projeto:**
   - [`core/`](#core-project)
     - [`__init__.py`](#core-init-py)
     - [`asgi.py`](#core-asgi-py)
     - [`settings.py`](#core-settings-py)
     - [`urls.py`](#core-urls-py)
     - [`wsgi.py`](#core-wsgi-py)
   - [`nginx/`](#nginx-folder)
     - [`nginx.conf`](#nginx-conf)
   - [`templates/`](#templates-folder)
     - [`icons/`](#icons-folder)
     - [`pages/`](#pages-folder)
       - [`index.html`](#index-html)
     - [`base.html`](#base-html)
   - [`users/`](#users-folder)
     - [`templates/`](#users-templates-folder)
       - `pages/`
         - [`create-account.html`](#users-create-account-html)
         - [`home.html`](#users-home-html)
     - [`adapters.py`](#users-adapters-py)
     - [`forms.py`](#users-forms-py)
     - [`url.py`](#users-url-py)
     - `views.py`
       - [`home_view()`](#users-view-home_view)
       - [`create_account()`](#users-view-create_account)
       - [`login_view()`](#users-view-login_view)
       - [`logout_view()`](#users-view-logout_view)
   - [`workspace/`](#workspace-folder)
     - `templates/`
       - `pages/`
         - [`workspace_home.html`](#workspace-workspace-home-html)
     - [`admin.py`](#workspace-admin-py)
     - [`forms.py`](#workspace-forms-py)
       - [`validate_file_size() function`](#workspace-forms-validate-file-size)
       - [`FolderForm() class`](#workspace-forms-folderform-class)
       - [`FileForm() class`](#workspace-forms-fileform-class)
       - [`FileUploadForm() class`](#workspace-forms-fileuploadform-class)
     - [`models.py`](#workspace-models-py)
       - [`workspace_upload_to() function`](#workspace-models-workspace-upload-to)
       - [`Folder() class`](#workspace-models-folder-class)
       - [`File() class`](#workspace-models-file-class)
     - [`url.py`](#workspace-url-py)
     - [`validators.py`](#workspace-validators-py)
       - [`validate_file_type()`](#workspace-validate-file-type)
       - [`validate_file_size()`](#workspace-validate-file-size)
       - [`validate_file()`](#workspace-validate-file)
     - `views.py`
       - [`workspace_home()`](#workspace-view-workspace-home)
       - [`create_folder()`](#workspace-view-create-folder)
       - [`upload_file()`](#workspace-view-upload-file)
       - [`build_breadcrumbs()`](#workspace-view-build-breadcrumbs)
       - [`delete_folder()`](#workspace-view-delete-folder)
       - [`delete_file()`](#workspace-view-delete-file)
       - [`rename_folder()`](#workspace-view-rename-folder)
       - [`rename_file()`](#workspace-view-rename-file)
       - [`_is_descendant`](#workspace-view-is-descendant)
       - [`move_item()`](#workspace-view-move-item)
 - **Configurações:**
   - [`[Google Auth] Configuração do Google OAuth (login social)`](#settings-google-auth)
   - [`[GitHub Auth] Configuração do GitHub OAuth (login social)`](#settings-github-auth)
<!---
[WHITESPACE RULES]
- Different topic = "100" Whitespace character.
- Same topic = "50" Whitespace character.
- Subtopic = "10" Whitespace character.
--->




































































































<!--- ( Introdução e Objetivos do Projeto ) --->

---

<div id="intro-to-the-project"></div>

## Introdução e Objetivos do Projeto

O **RAG Project** foi desenvolvido para solucionar um problema recorrente na *Secretaria de Educação*, onde trabalho (Remígio-PB):

> A **"ausência de um mecanismo de consulta"** em um grande número de pastas, arquivos e formatos.

Para enfrentar esse desafio, o projeto adota uma arquitetura baseada em *Retrieval-Augmented Generation (RAG)*, integrando técnicas de *Processamento de Linguagem Natural (NLP)*, *modelos de linguagem (LLMs)* e *mecanismos de busca vetorial*. O sistema permite transformar dados institucionais estáticos em um repositório consultável e responsivo.

### 🎯 Objetivos Técnicos

 - Centralizar documentos institucionais de forma estruturada.
 - Indexar arquivos através de embeddings semânticos.
 - Realizar consultas híbridas (vetorial + keyword).
 - Fornecer respostas geradas por LLMs baseadas exclusivamente nos dados indexados.
 - Garantir rastreabilidade e auditoria das fontes utilizadas nas respostas.

### 🏗️ Arquitetura do Sistema

A solução é dividida em *quatro camadas* principais:

 - **1. Ingestão de Dados:**
   - Extração de conteúdo de PDFs, DOCXs, planilhas e documentos administrativos.
   - Normalização de texto e limpeza semântica.
   - Pipeline automatizado de pré-processamento (fragmentação, tokenização, chunking).
 - **2. Indexação e Armazenamento:**
   - Geração de embeddings com modelo compatível com LLM escolhido.
   - Armazenamento em banco vetorial.
 - **3. Recuperação da Informação (Retrieval):**
   - Recuperação baseada em similaridade vetorial.
   - Suporte a filtros estruturados (metadata filtering).
   - Opcional: rerankers para melhorar precisão do top-k.
 - **4. Geração da Resposta (LLM Layer):**
   - Pipeline RAG com prompt engineering focado em:
     - grounding em documentos institucionais;
     - citar fontes;
     - evitar alucinações;
     - manter conformidade administrativa.
   - Respostas são geradas usando LLMs locais ou hospedados (OpenAI, Azure, vLLM, etc.).




































































































<!--- ( Estrutura do Projeto ) --->









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

**Imports:** [core/settings.py](core/settings.py)
```python
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```

 - `import os`
   - Importa o módulo padrão `os` do Python; usado para operar com variáveis de ambiente `(os.getenv)` e outras utilidades do *SO*.
 - `from pathlib import Path`
   - `Path` é a forma recomendada moderna de manipular caminhos (substitui `os.path` em muitas situações) e é usado aqui para construir `BASE_DIR` e referências a diretórios dentro do projeto.
 - `from dotenv import load_dotenv`
   - Importa a função `load_dotenv` do pacote *python-dotenv*.
   - Essa função lê um arquivo `.env` e carrega suas chaves como variáveis de ambiente — útil em desenvolvimento para não expor segredos no código.
 - `load_dotenv()`
   - Chama a função (Cria uma instância) para efetivamente carregar as variáveis definidas no `.env` (se existir).
   - Após isso, `os.getenv(...)` pode ler essas variáveis.

**Diretório raiz do projeto:** [core/settings.py](core/settings.py)
```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

 - `__file__`
   - Caminho do arquivo [settings.py](core/settings.py).
 - `Path(__file__)`
   - Transforma em objeto Path.
 - `.resolve()`
   - Converte para um caminho absoluto.
 - `.parent.parent`
   - Sobe duas pastas (ex.: `core/settings.py` → `core/` → `raiz do projeto`).

**Chave secreta usada pelo Django para criptografia e segurança interna:** [core/settings.py](core/settings.py)
```python
SECRET_KEY = 'django-insecure-ntyi#32b20l03ioo=3tr=1j8snafe(7*l=#)u&6+rdyrk)6v7f'
```

 - Valor crítico que o Django usa para:
   - sessões,
   - geração de tokens,
   - hashes internos,
   - validação de assinaturas.
 - Nunca deve ser exposto em produção.
 - **NOTE:** Em ambiente real, você deve usar `os.getenv("SECRET_KEY")`.

**Ativa ou desativa o modo de depuração do Django:** [core/settings.py](core/settings.py)
```python
DEBUG = True
```

 - Quando True:
   - Django mostra páginas de erro com informações sensíveis,
   - recarrega o servidor automaticamente,
   - não aplica certas proteções de segurança.
 - **NOTE:** Nunca usar *True* em produção.

**Lista de domínios que o Django aceita como válidos para requisições:** [core/settings.py](core/settings.py)
```python
ALLOWED_HOSTS = []
```

 - Lista vazia:
   - Em desenvolvimento funciona bem com DEBUG=True.
   - Em produção com DEBUG=False o Django bloqueia todas as requisições.
 - Quando for para produção, configure algo como:
   - `ALLOWED_HOSTS = ["example.com", "localhost", "127.0.0.1"]`

#### `INSTALLED_APPS = []`

`INSTALLED_APPS` registra todos os aplicativos que o Django deve carregar:

 - apps padrão,
 - apps de terceiros (ex.: allauth),
 - e os apps locais do seu projeto.

Cada entrada ativa *sinalização de modelos*, *rotas estáticas*, *templates* e *hooks de inicialização*.

[core/settings.py](core/settings.py)
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
    "workspace",
]
```

#### `MIDDLEWARE = []`

> `MIDDLEWARE` é uma lista ordenada de componentes que processam a requisição/resposta globalmente.

Cada middleware pode inspecionar/alterar request/response e fornece funcionalidades transversais:

 - segurança,
 - sessão,
 - CSRF,
 - autenticação,
 - mensagens,
 - proteção contra clickjacking,
 - etc...

[core/settings.py](core/settings.py)
```python
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

 - `allauth.account.middleware.AccountMiddleware`
   - Middleware do allauth (comentado como “Novo middleware exigido pelo Django Allauth”) — provê integrações necessárias para fluxos de conta/social. (Observação: verifique a documentação do allauth; alguns setups funcionam sem esse middleware, mas aqui o projeto exige.)
 - `django.contrib.messages.middleware.MessageMiddleware`
   - Integra as mensagens (django.contrib.messages) com a sessão e templates.
 - `django.middleware.clickjacking.XFrameOptionsMiddleware`
   - Previne que o site seja embutido em iframes (configura o header X-Frame-Options).

#### `ROOT_URLCONF = 'core.urls'`

Indica o módulo que contém as definições de URL raiz do projeto. É o ponto de entrada para o roteamento das views.

[core/settings.py](core/settings.py)
```python
ROOT_URLCONF = 'core.urls'
```

 - `ROOT_URLCONF = 'core.urls'`
   - O Django importará `core.urls (arquivo core/urls.py)` para buscar as patterns de URL iniciais.
   - Esse módulo normalmente inclui *"urlpatterns"* que dirigem as rotas para apps, admin, endpoints estáticos, etc.

#### `TEMPLATES = []`

Configura o mecanismo de templates do Django:

 - Onde procurar templates,
 - se habilitar descoberta por app (APP_DIRS),
 - e quais *"context processors"* estarão disponíveis em todos os templates (variáveis automaticamente injetadas).

[core/settings.py](core/settings.py)
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
```

 - `'DIRS': [BASE_DIR / 'templates']`
   - Lista de diretórios externos (fora de apps) onde o Django vai procurar templates.
   - Aqui: project_root/templates/.
 - `'APP_DIRS': True`
   - Se True, o Django procura automaticamente por um diretório **templates/** dentro de cada app listado em `INSTALLED_APPS`.
 - `'OPTIONS': { 'context_processors': [...] }`
   - Context processors são funções que injetam variáveis (contexto) automaticamente em todos os templates.
   - `django.template.context_processors.request`
     - Adiciona request ao contexto do template (necessário para django-allauth e para checar request.user, request.path etc).

#### `AUTHENTICATION_BACKENDS`

> Define os backends de autenticação que o Django tentará para autenticar um usuário.

**NOTE:**  
A ordem importa: o Django tenta cada backend até um autenticar com sucesso.

[core/settings.py](core/settings.py)
```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",            # Seu login normal
    "allauth.account.auth_backends.AuthenticationBackend",  # Login social
]
```

 - `"django.contrib.auth.backends.ModelBackend"`
   - Backend padrão que verifica username/password no modelo User.
 - `"allauth.account.auth_backends.AuthenticationBackend"`
   - Backend do allauth que permite autenticação via provedores sociais e integra com o fluxo de contas do allauth. Mantém compatibilidade com o backend padrão.

> **NOTE:**  
> A presença dos dois permite tanto logins tradicionais (username/password) quanto logins via OAuth (Google/GitHub).

#### `DATABASES = {}`

> Configura o(s) banco(s) de dados do projeto.

Aqui está configurado PostgreSQL e as credenciais são lidas de variáveis de ambiente (boa prática): assim o container/ambiente pode prover *POSTGRES_DB*, *POSTGRES_USER*, etc.

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

[core/settings.py](core/settings.py)
```python
# Database
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

**O que os.getenv('VAR', 'default') faz, exatamente?**  
`os.getenv` vem do módulo padrão `os` e faz o seguinte:

 - Tenta ler a variável de ambiente chamada 'VAR' (por exemplo POSTGRES_DB);
 - Se existir, retorna o valor da variável de ambiente;
 - Se não existir, retorna o valor padrão passado como segundo argumento ('default').

**Por que às vezes PASSAMOS um valor padrão (default) no código?**

 - *Conforto no desenvolvimento local:* evita quebrar o projeto se você esquecer de definir `.env`.
 - *Documentação inline:* dá uma ideia do nome esperado (easy_rag, 5432, etc.).
 - *Teste rápido:* você pode rodar `manage.py` localmente sem carregar variáveis.

> **NOTE:**  
> Mas atenção: os valores padrões não devem conter segredos reais (ex.: supersecret) no repositório público — isso é um risco de segurança.

**Por que não você não deveria colocar senhas no código?**

 - Repositórios (Git) podem vazar ou ser lidos por terceiros.
 - Código pode acabar em backups, imagens Docker, etc.
 - Difícil rotacionar/chavear senhas se espalhadas pelo repositório.

> **Regra prática:**  
> - *"NUNCA"* colocar credenciais reais em `settings.py`.
> - Use `.env` (não comitado) ou um *"secret manager"*.

#### `Configurações de "Internacionalização"`

[core/settings.py](core/settings.py)
```python
# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
```

 - `LANGUAGE_CODE = "pt-br"`
   - "pt-br" indica que o Django deve usar português do Brasil como idioma padrão.
   - Afeta mensagens de erro, validação de formulários e textos gerados pelo framework.
 - `TIME_ZONE = "America/Sao_Paulo"`
   - "America/Sao_Paulo" ajusta o Django para o fuso horário oficial de São Paulo.
   - Usado na exibição e manipulação de datas/horas quando o Django converte para o timezone local.
 - `USE_I18N = True`
   - True habilita o suporte a múltiplos idiomas.
   - Necessário para traduções, uso de arquivos `.po` e recursos multilíngues.
 - `USE_TZ = True`
   - True faz com que o Django armazene tudo em UTC no banco.
   - Conversões para o fuso horário local (especificado em TIME_ZONE) acontecem apenas na exibição.
   - Melhora precisão e evita erros com horário de verão.

#### `Configurações de Arquivos Estáticos (STATIC)`

Essas linhas configuram como o Django encontra, organiza e serve arquivos estáticos — como *CSS*, *JavaScript* e *imagens*.

[core/settings.py](core/settings.py)
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

 - `STATIC_URL = '/static/'`
   - Define a URL base onde os arquivos estáticos serão acessados no navegador.
   - Exemplo: um arquivo `style.css` pode ser servido em `/static/style.css`.
   - É usado pelo Django ao gerar caminhos com `{% static %}` nos templates.
 - `STATICFILES_DIRS = [BASE_DIR / 'static']`
   - Indica para o Django onde estão os arquivos estáticos criados por você (CSS, JS, imagens do projeto).
 - `STATIC_ROOT = BASE_DIR / 'staticfiles'`
   - Diretório onde o Django coloca todos os arquivos estáticos coletados quando você executa:
     - `python manage.py collectstatic`
     - `python manage.py collectstatic --no-input`
   - Criado para produção, onde o servidor web serve os arquivos prontos e organizados.
   - `static/` → onde ficam seus arquivos no desenvolvimento
   - `staticfiles/` → onde ficam os arquivos finais para produção

#### `Configurações de Arquivos de Mídia (MEDIA)`

Essas configurações determinam onde o Django armazena e como ele disponibiliza arquivos enviados pelo usuário — como *fotos de perfil*, *documentos*, *uploads em formulários* etc.

[core/settings.py](core/settings.py)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

 - `MEDIA_URL = '/media/'`
   - Define a URL base usada para acessar arquivos de mídia no navegador.
   - Exemplo: se um usuário envia `foto.png`, ela pode ser acessada em:
     - `/media/foto.png`
 - `MEDIA_ROOT = BASE_DIR / 'media'`
   - Define o diretório físico onde o Django vai armazenar todos os arquivos enviados pelo usuário.
   - `BASE_DIR / 'media'` → cria/usa a pasta `media/` na raiz do projeto.
   - O Django salva os uploads dentro dela, geralmente usando *"FileField"* ou *"ImageField"*.

#### `Configurações de autenticação do Django + Allauth`

Esse bloco agrupa configurações relacionadas à **autenticação de usuários** e ao pacote django-allauth:

 - controle de qual “site” está ativo (útil para logins sociais),
 - redirecionamentos pós-login/logout,
 - método de login aceito,
 - campos exigidos no cadastro,
 - política de verificação de e-mail e adapters personalizados (por exemplo para suprimir envio de e-mail em desenvolvimento).

[core/settings.py](core/settings.py)
```python
SITE_ID = 2

LOGIN_REDIRECT_URL = "/home/"  # ou o nome da rota que preferir
LOGOUT_REDIRECT_URL = "/"      # para onde o usuário vai depois do logout
SOCIALACCOUNT_LOGIN_ON_GET = True  # Login imediato ao clicar no link do provedor

# Permitir login apenas com username (pode ser {'username', 'email'} se quiser os dois)
ACCOUNT_LOGIN_METHODS = {"username"}

# Campos obrigatórios no cadastro (asterisco * indica que o campo é requerido)
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"     # "mandatory" em produção

ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapter.NoMessageSocialAccountAdapter"
```

 - `SITE_ID = 2`
   - O django-allauth (e outros apps) consultam SITE_ID para construir URLs absolutas, callbacks OAuth (redirect URIs) e para associar configurações por site.
   - Usar **"2"** indica que você tem uma linha no banco **id=2** representando o domínio/URL ativo; em dev muitas vezes é 1, em ambientes com múltiplos sites pode ser outro valor.
 - `LOGIN_REDIRECT_URL = "/home/"`
   - URL para onde o usuário é redirecionado após um login bem-sucedido.
   - Pode ser uma rota absoluta ("/home/") ou o reverse() name de uma view (ex.: "/dashboard/" ou reverse_lazy("home")). É o destino padrão quando next não é fornecido.
 - `LOGOUT_REDIRECT_URL = "/"`
   - URL para onde o usuário é redirecionado após o logout.
   - Aqui é a raiz do site ("/").
   - Pode apontar para uma landing page, página de login, etc.
 - `SOCIALACCOUNT_LOGIN_ON_GET = True`
   - Marcado como `True`, o usuário não verá a tela intermediária do Django:
     - */accounts/google/login/*
   - E sim que ao clicar no botão ele será redirecionado imediatamente para o Google ou GitHub.  
 - `ACCOUNT_LOGIN_METHODS = {"username"}`
   - Define quais campos são aceitos para autenticação no fluxo de cadastro/login do allauth.
   - Usando *{"username"}* o site permite apenas login por nome de usuário.
   - Se quiser permitir email também, use {"username", "email"} (ou apenas {"email"} para só e-mail).
   - **NOTE:** A escolha impacta formulários, validações e UX.
 - `ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]`
   - Lista os campos que aparecem (e são obrigatórios, quando marcados com *) no formulário de signup do allauth.
 - `ACCOUNT_EMAIL_VERIFICATION = "optional"`
   - Política de verificação de e-mail do allauth.
   - valores comuns:
     - "none" — não exige verificação;
     - "optional" — permite, mas não impede login sem verificação;
     - "mandatory" — usuário não pode usar a conta até verificar o e-mail.
   - **NOTE:** Em ambiente de produção é recomendado "mandatory" para garantir que e-mails sejam confiáveis.
 - `ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"`
 - `SOCIALACCOUNT_ADAPTER = "users.adapter.NoMessageSocialAccountAdapter"`
   - Aqui estamos informando ao Allauth que queremos usar classes personalizadas que removem ou alteram o envio de mensagens (como avisos de login, erros, confirmações etc.).
   - Assim, o Allauth deixa de adicionar automaticamente mensagens via django.contrib.messages, evitando poluição visual ou mensagens redundantes no frontend.










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

<div id="nginx-folder"></div>

## `nginx/`

> A pasta `nginx/` geralmente existe em projetos que precisam de um **Servidor NGINX** para:

 - Servir páginas estáticas (HTML, CSS, JS);
 - Roteamento de frontend (React, Vue, Angular);
 - Fazer reverse proxy para APIs (ex.: /api → backend);
 - Gerenciar SSL/HTTPS;
 - Fazer cache, compressão, headers de segurança;
 - Balancear tráfego (em setups maiores).

Por exemplo:

```bash
nginx/
 ├── nginx.conf      ← configuração principal
 ├── default.conf    ← configuração do server (separada, opcional)
 ├── ssl/            ← certificados HTTPS (em produção)
 └── conf.d/         ← configurações extras
```










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

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```conf
server {

}
```

A parte do códigm acima representa um servidor virtual — ou seja, as regras de como o NGINX deve se comportar quando recebe requisições em um domínio ou porta específica.

```conf
server {
    listen 80;
    server_name _;

    # 🔓 Permitir uploads (dados enviados pelo usuário) de qualquer tamanho.
    # > O Django quem vai validar isso.
    client_max_body_size 0;
}
```

 - `listen 80;`
   - Define qual porta o servidor ouvirá: *80 (HTTP padrão)*.
 - `server_name _;`
   - Define para quais domínios esse servidor responde.
   - O `_` é um coringa, indicando *“qualquer nome de servidor”*.
   - É muito usado para servidores default.
 - `client_max_body_size 0;`
   - Define o tamanho máximo permitido para uploads.
   - 0 = Ilimitado.
   - Importante quando você trabalha com upload de arquivos grandes (PDF, imagens, vídeos, etc.).

```conf
server {

    # Servir arquivos estáticos diretamente
    location /static/ {
        alias /code/staticfiles/;
        expires 30d;
        access_log off;
        autoindex on;
    }

}
```

 - `location /static/ { ... }`
   - Define uma regra para todas as requisições que começam com /static/.
   - `alias /code/staticfiles/;`
     - Associa a URL */static/* ao diretório físico */code/staticfiles/*.
     - Exemplo: */static/style.css* → */code/staticfiles/style.css*.
   - `expires 30d;`
     - Instrui o navegador a cachear os arquivos por 30 dias.
     - Reduz requisições e melhora a performance.
   - `access_log off;`
     - Desativa o registro de logs de acesso para essas requisições.
     - Evita poluição dos logs com arquivos estáticos.
   - `autoindex on;`
     - Habilita a listagem automática dos arquivos do diretório se não existir um arquivo index.
     - Útil para desenvolvimento ou inspeção, *"mas geralmente desativado em produção"*.

```conf
server {

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

 - `location / { ... }`
   - Define uma regra que captura todas as requisições que não foram tratadas por outros blocos location (como */static/* e */media/*).
   - `proxy_pass http://web:8000;`
     - Encaminha a requisição para o serviço web na porta 8000.
     - Normalmente esse serviço é o container do Django rodando com Uvicorn/Gunicorn.
   - `proxy_set_header Host $host;`
     - Repassa o host original da requisição para o Django.
     - Importante para ALLOWED_HOSTS, geração de URLs e comportamento correto de multi-domínio.
   - `proxy_set_header X-Real-IP $remote_addr;`
     - Envia para o Django o IP real do cliente.
     - Permite logs, auditoria e regras baseadas em IP.
   - `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
     - Mantém uma lista encadeada de IPs pelos quais a requisição passou.
     - Útil quando há múltiplos proxies ou balanceadores.
   - `proxy_set_header X-Forwarded-Proto $scheme;`
     - Informa ao Django se a requisição original foi feita via *http* ou *https*.
     - Essencial para gerar URLs corretas e evitar problemas com redirecionamentos e cookies seguros.


















































<!--- ( templates/ ) --->

---

<div id="templates-folder"></div>

## `templates/`

> O diretório `raiz/templates/` é onde ficam todos os arquivos HTML **globais** da aplicação Django.










---

<div id="icons-folder"></div>

## `icons/`

> O diretório `raiz/templates/icons/` é onde ficam os arquivos SVG dos ícones usados na aplicação.

Por exemplo:

 - [github.svg.html](templates/icons/github.svg.html)
   - Ícone do GitHub em SVG salvo em HTML.
 - [google.svg.html](templates/icons/google.svg.html)
   - Ícone do Google em SVG salvo em HTML.










---

<div id="pages-folder"></div>

## `pages/`

> O diretório `raiz/templates/pages/` é onde ficam os templates das páginas genéricas do seu site.

**Quando é utilizado?**

 - **Páginas genéricas:** Home, Sobre, Contato, FAQ;
 - **Conteúdo estático:** Termos de Uso, Política de Privacidade;
 - **Landing pages:** Páginas de marketing ou campanhas;
 - **Páginas públicas:** Conteúdo acessível sem login.










---

<div id="index-html"></div>

## `index.html`

O [index.html](templates/pages/index.html) é a `landing page` da nossa aplicação.

> **Mas, afinal, o que é um "landing page"?**

Uma `landing page (pública no nosso caso)` geralmente contem:

 - Apresentação do produto/serviço.
 - Botões de “Entrar” e “Cadastrar”.
 - Sessões com informações sobre a empresa.
 - Depoimentos, preços, etc.

[index.html](templates/pages/index.html)
```html
{% extends "base.html" %}
{% load socialaccount %}

{% block content %}

    <!-- Main Content -->
    <main class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">

            <!-- Card -->
            <div class="max-w-md w-full space-y-8 bg-white py-8 px-6 shadow rounded-lg">

                <!-- Logo / Title -->
                <div class="mb-6 text-center">
                    <h2 class="mt-4 text-2xl font-semibold text-gray-900">RAG Project</h2>
                    <p class="mt-1 text-sm text-gray-500">Faça login para acessar seu painel</p>
                </div>

                {% if messages %}
                    <div class="mb-4">
                        {% for message in messages %}
                            <div class="text-red-600 bg-red-100 border border-red-200 rounded-md px-4 py-2 text-sm">
                                {{ message }}
                            </div>
                        {% endfor %}
                    </div>
                {% endif %}

                <!-- Form -->
                <form method="post" action="" class="space-y-6">
                    {% csrf_token %}

                    <!-- Username -->
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">Usuário</label>
                        <div class="mt-1">
                            <input
                                id="username"
                                name="username"
                                type="text"
                                autocomplete="username"
                                required
                                class="appearance-none
                                       block w-full px-3
                                       py-2 border border-gray-300
                                       rounded-md shadow-sm
                                       placeholder-gray-400
                                       focus:outline-none focus:ring-2
                                       focus:ring-blue-500
                                       focus:border-blue-500 sm:text-sm">
                        </div>
                    </div>

                    <!-- Password -->
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
                        <div class="mt-1">
                            <input
                                id="password"
                                name="password"
                                type="password"
                                autocomplete="current-password"
                                required
                                class="appearance-none
                                       block w-full px-3 py-2
                                       border border-gray-300
                                       rounded-md shadow-sm
                                       placeholder-gray-400
                                       focus:outline-none
                                       focus:ring-2
                                       focus:ring-blue-500
                                       focus:border-blue-500
                                       sm:text-sm">
                        </div>
                    </div>

                    <!-- Submit -->
                    <div>
                        <button type="submit"
                            class="w-full flex
                                   justify-center
                                   py-2 px-4 border
                                   border-transparent
                                   rounded-md shadow-sm
                                   text-sm font-medium
                                   text-white bg-blue-600
                                   hover:bg-blue-700
                                   focus:outline-none
                                   focus:ring-2
                                   focus:ring-offset-2
                                   focus:ring-blue-500">
                            Entrar
                        </button>
                    </div>
                </form>

                <!-- Divider -->
                <div class="mt-6 relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="bg-white px-2 text-gray-500">ou continuar com</span>
                    </div>
                </div>

                <!-- Social login buttons -->
                <div class="mt-6 grid grid-cols-2 gap-3">
                    <!-- Google -->
                    <div>
                        <a href="{% provider_login_url 'google' %}"
                        class="w-full inline-flex justify-center
                               items-center py-2 px-4 border
                               border-gray-300 rounded-md
                               shadow-sm bg-white hover:bg-gray-50">
                            {% include "icons/google.svg.html" %}
                            <span class="text-sm font-medium text-gray-700">Google</span>
                        </a>
                    </div>

                    <!-- GitHub -->
                    <div>
                        <a href="{% provider_login_url 'github' %}"
                        class="w-full inline-flex justify-center
                               items-center py-2 px-4 border
                               border-gray-300 rounded-md
                               shadow-sm bg-white hover:bg-gray-50">
                            {% include "icons/github.svg.html" %}
                            <span class="text-sm font-medium text-gray-700">GitHub</span>
                        </a>
                    </div>
                </div>

                <!-- Footer: cadastrar -->
                <p class="mt-6 text-center text-sm text-gray-600">
                    Não tem conta?
                    <a href="{% url 'create-account' %}" class="font-medium text-blue-600 hover:text-blue-700">
                        Cadastrar
                    </a>
                </p>

            </div>

    </main>
{% endblock %}
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```html
{% load socialaccount %}
```

 - `{% load socialaccount %}`
   - Carrega as template tags do *django-allauth* para login social.
   - Permite usar funções como:
     - {% provider_login_url 'google' %}
     - {% provider_login_url 'github' %}
   - **NOTE:** Sem essa linha, essas tags gerariam erro no template.

```html
<!-- Main Content -->
<main class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">

</main>
```

 - Elemento principal da página que estrutura o layout central do conteúdo.
 - Esse `<main>` é o responsável por deixar o card de login perfeitamente centralizado e responsivo em qualquer tamanho de tela.
   - `<main>` → tag semântica do HTML que indica o conteúdo principal da página.
   - `min-h-screen` → garante que o elemento tenha no mínimo a altura total da tela.
   - `flex` → ativa o Flexbox para organizar os elementos internos.
   - `items-center` → centraliza os elementos verticalmente.
   - `justify-center` → centraliza os elementos horizontalmente.
   - `py-12` → adiciona espaçamento vertical (padding top e bottom).
   - `px-4` → padding horizontal padrão para telas pequenas.
   - `sm:px-6` → padding horizontal maior em telas médias (sm).
   - `lg:px-8` → padding horizontal ainda maior em telas grandes (lg).

```html
<!-- Card -->
<div class="max-w-md w-full space-y-8 bg-white py-8 px-6 shadow rounded-lg">

</div>
```

 - Container visual que funciona como o card central da tela de login.
 - Esse bloco é o responsável pelo visual limpo e centralizado do formulário de login.
   - `<div>` → elemento de bloco usado como container visual.
   - `max-w-md` → limita a largura máxima do card (tamanho médio), evitando que ele fique largo demais.
   - `w-full` → faz o card ocupar 100% da largura disponível até o limite definido.
   - `space-y-8` → adiciona espaçamento vertical uniforme entre os elementos filhos.
   - `bg-white` → define o fundo do card como branco.
   - `py-8` → padding vertical interno (top e bottom).
   - `px-6` → padding horizontal interno (left e right).
   - `shadow` → adiciona sombra, criando efeito de elevação.
   - `rounded-lg` → arredonda os cantos do card.

```html
<!-- Logo / Title -->
<div class="mb-6 text-center">
    <h2 class="mt-4 text-2xl font-semibold text-gray-900">RAG Project</h2>
    <p class="mt-1 text-sm text-gray-500">Faça login para acessar seu painel</p>
</div>
```

 - Bloco responsável por exibir o título e a descrição da página de login.
   - `<div class="mb-6 text-center">`
     - `<div>` → container que agrupa título e subtítulo.
     - `mb-6` → adiciona margem inferior para separar este bloco do conteúdo seguinte.
     - `text-center` → centraliza o texto horizontalmente.
   - `<h2 class="mt-4 text-2xl font-semibold text-gray-900">RAG Project</h2>`
     - `<h2>` → título de segundo nível, usado como cabeçalho da página.
     - `mt-4` → adiciona margem superior, criando espaço em relação a elementos acima.
     - `text-2xl` → define tamanho grande para o texto do título.
     - `font-semibold` → aplica peso de fonte semi-negrito.
     - `text-gray-900` → usa um tom escuro de cinza para melhor contraste e legibilidade.
   - `<p class="mt-1 text-sm text-gray-500">Faça login para acessar seu painel</p>`
     - `<p>` → parágrafo usado como texto auxiliar.
     - `mt-1` → pequeno espaçamento superior em relação ao título.
     - `text-sm` → tamanho de fonte menor, indicando informação secundária.
     - `text-gray-500` → tom de cinza mais claro, reforçando hierarquia visual.

```html
{% if messages %}
    <div class="mb-4">
        {% for message in messages %}
            <div class="text-red-600 bg-red-100 border border-red-200 rounded-md px-4 py-2 text-sm">
                {{ message }}
            </div>
        {% endfor %}
    </div>
{% endif %}
```

 - Bloco responsável por exibir mensagens do sistema (erros, avisos ou feedbacks) para o usuário.
 - Esse bloco garante que o usuário receba feedback claro e visível, especialmente em casos de erro de login ou validação.
   - `{% if messages %}`
     - Verifica se existe pelo menos uma mensagem no contexto.
     - *"messages"* vem do framework de mensagens do Django (django.contrib.messages).
   - `{% for message in messages %}`
     - Itera sobre cada mensagem disponível no contexto.
     - Cada *"message"* representa um feedback enviado pelo backend (ex.: erro de login).
   - `<div class="text-red-600 bg-red-100 border border-red-200 rounded-md px-4 py-2 text-sm">`
     - Container visual da mensagem.
     - `text-red-600` → texto vermelho, indicando erro.
     - `bg-red-100` → fundo vermelho claro.
     - `border border-red-200` → borda sutil vermelha.
     - `rounded-md` → cantos arredondados.
     - `px-4 py-2` → espaçamento interno.
     - `text-sm` → tamanho de fonte reduzido.
   - `{{ message }}`
     - Renderiza o conteúdo da mensagem enviada pelo Django.
     - Pode ser texto de erro, aviso ou confirmação.

```html
<!-- Form -->
<form method="post" action="" class="space-y-6">
    {% csrf_token %}
</form>
```

 - Formulário responsável por enviar os dados de login do usuário para o backend.
 - Esse formulário funciona como a base do login tradicional, onde o usuário informa username e senha para autenticação.
 - `<form method="post" action="" class="space-y-6">`
   - `<form>` → elemento HTML que agrupa campos e botões de envio.
   - `method="post"` → define que os dados serão enviados via POST, método adequado para informações sensíveis como senha.
   - `action=""` → indica que o formulário será enviado para a URL atual.
   - `class="space-y-6"` → adiciona espaçamento vertical entre os elementos internos do formulário.
   - `{% csrf_token %}` → Proteção de segurança obrigatória contra ataques CSRF em formulários Django:
     - Gera um token CSRF único para a sessão do usuário.
     - Esse token é inserido como um campo oculto no formulário HTML.
     - O Django valida esse token ao receber o POST para garantir que a requisição veio do próprio site.
     - Protege contra ataques do tipo Cross-Site Request Forgery (CSRF).
     - **NOTE:** Sem essa linha, formulários POST no Django gerariam erro 403 (Forbidden) por padrão.

```html
<!-- Username -->
<div>
    <label for="username" class="block text-sm font-medium text-gray-700">Usuário</label>
    <div class="mt-1">
        <input
            id="username"
            name="username"
            type="text"
            autocomplete="username"
            required
            class="appearance-none
                   block w-full px-3
                   py-2 border border-gray-300
                   rounded-md shadow-sm
                   placeholder-gray-400
                   focus:outline-none focus:ring-2
                   focus:ring-blue-500
                   focus:border-blue-500 sm:text-sm">
    </div>
</div>
```

 - Campo de entrada para o username do usuário.
 - `id="username"`
   - Identificador único do elemento no HTML.
   - Usado pelo `<label for="username">` para associar o rótulo ao campo.
   - Também pode ser usado por JavaScript e CSS.
 - `name="username"`
   - Nome do campo enviado ao backend no POST.
   - O Django usa esse valor para acessar o dado com:
     - `request.POST["username"]`
   - É essencial para que o servidor receba o valor corretamente.
 - `type="text"`
   - Define que o campo aceita texto livre.
   - Usado para entrada de nome de usuário (não oculta caracteres).
 - `autocomplete="username"`
   - Instrui o navegador a sugerir nomes de usuário salvos.
   - Melhora a experiência do usuário ao preencher o formulário.
   - Segue o padrão HTML para campos de autenticação.
 - `required`
   - Torna o campo **obrigatório no lado do cliente**.
   - O navegador impede o envio do formulário se estiver vazio.
   - Não substitui validação no backend, apenas complementa.

```html
<!-- Divider -->
<div class="mt-6 relative">
    <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-200"></div>
    </div>
    <div class="relative flex justify-center text-sm">
        <span class="bg-white px-2 text-gray-500">ou continuar com</span>
    </div>
</div>
```

 - Bloco que insere uma divisão visual no formulário, separando o login tradicional do login social.
 - Esse bloco cria uma linha divisória visual com a frase **"ou continuar com"**, separando o formulário de login tradicional dos botões de login social.
 - Ideal para melhorar a UX, tornando a página mais clara e organizada.

```html
<!-- Social login buttons -->
<div class="mt-6 grid grid-cols-2 gap-3">
    <!-- Google -->
    <div>
        <a href="{% provider_login_url 'google' %}"
        class="w-full inline-flex justify-center
                items-center py-2 px-4 border
                border-gray-300 rounded-md
                shadow-sm bg-white hover:bg-gray-50">
            {% include "icons/google.svg.html" %}
            <span class="text-sm font-medium text-gray-700">Google</span>
        </a>
    </div>

    <!-- GitHub -->
    <div>
        <a href="{% provider_login_url 'github' %}"
        class="w-full inline-flex justify-center
                items-center py-2 px-4 border
                border-gray-300 rounded-md
                shadow-sm bg-white hover:bg-gray-50">
            {% include "icons/github.svg.html" %}
            <span class="text-sm font-medium text-gray-700">GitHub</span>
        </a>
    </div>
</div>
```

 - `<a href="{% provider_login_url 'google' %}">`
   - Gera dinamicamente a URL de login com o Google usando o django-allauth.
   - `{% provider_login_url 'google' %}` cria a URL OAuth correta (redirect, scopes, callbacks).
   - Evita URLs fixas e garante compatibilidade com ambientes diferentes (dev, prod).
 - `{% include "icons/google.svg.html" %}`
   - Insere o SVG do ícone do Google diretamente no HTML.
   - Reutiliza o arquivo parcial localizado em **templates/icons/google.svg.html**.
   - Não faz requisição extra e permite estilização com CSS/Tailwind.
 - `<a href="{% provider_login_url 'github' %}">`
   - Gera dinamicamente a URL de login com o GitHub via django-allauth.
   - O Allauth cuida de todo o fluxo OAuth (autorização, callback e criação/vinculação do usuário).
 - `{% include "icons/github.svg.html" %}`
   - Insere o SVG do ícone do GitHub diretamente no HTML.










---

<div id="base-html"></div>

## `base.html`

Este é um *template base* do Django que serve como estrutura principal (layout) para todas as outras páginas da aplicação.

 - Ele define a estrutura HTML básica;
 - Configurações de meta tags;
 - Carrega bibliotecas via CDN;
 - Fornece blocos que podem ser sobrescritos por templates filhos.

[base.html](templates/base.html)
```html
<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}{% endblock title %}</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        {% block head %}{% endblock head %}
    </head>
    <body class="min-h-screen bg-[#343541]">
        {% block content %}{% endblock content %}
        {% block scripts %}{% endblock scripts %}
    </body>
</html>
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

 - `<!DOCTYPE html>`
   - Declaração do tipo de documento HTML5, informando ao navegador que este é um documento HTML moderno.
 - `lang="pt-br"`
   - Define o idioma da página.
 - `<html></html>`


















































<!--- ( user/ ) --->

---

<div id="users-folder"></div>

## `user/`

> **O app users é responsável por gerenciar tudo relacionado aos usuários da aplicação.**

**Por que criar um app separado?**  
Django já vem com um sistema de autenticação embutido (`django.contrib.auth`), mas criamos um app "users" separado para:

 - Customizar o modelo de usuário - Adicionar campos extras;
 - Organizar o código - Manter tudo relacionado a usuários em um lugar;
 - Facilitar manutenção - Separação de responsabilidades.

### `Quando é utilizado?`

O app **"users"** é usado sempre que você precisa:

 - **Autenticação:** Login, logout, registro de novos usuários;
 - **Perfis de usuário:** Informações adicionais além das básicas (nome, email, senha);
 - **Permissões e grupos:** Controlar o que cada usuário pode fazer;
 - **Gerenciamento de contas:** Edição de perfil, troca de senha, recuperação de senha;
 - **Informações personalizadas:** Avatar, bio, preferências, etc.










---

<div id="users-templates-folder"></div>

## `templates/`

> O diretório `users/templates/` é onde ficam os templates do app users.










---

<div id="users-create-account-html"></div>

## `create-account.html`

> Essa página (HTML) vai ser responsável por exibir o formulário de criação de uma nova conta de usuário.

[create-account.html](users/templates/pages/create-account.html)
```html
{% extends "base.html" %}

{% block title %}Criar Conta{% endblock %}

{% block content %}

    <main class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">

            <!-- Card -->
            <div class="max-w-md w-full space-y-8 bg-white py-8 px-6 shadow rounded-lg">

                <!-- Logo / Title -->
                <div class="mb-6 text-center">
                    <h2 class="mt-4 text-2xl font-semibold text-gray-900">Criar Conta</h2>
                    <p class="mt-1 text-sm text-gray-500">
                        Preencha os campos abaixo para se cadastrar
                    </p>
                </div>

                {% if messages %}
                    <div class="mb-4">
                        {% for message in messages %}
                            <div class="text-red-600 bg-red-100 border
                                        border-red-200 rounded-md px-4
                                        py-2 text-sm">
                                {{ message }}
                            </div>
                        {% endfor %}
                    </div>
                {% endif %}

                <!-- Form -->
                <form method="post" action="" class="space-y-6">
                    {% csrf_token %}

                    {{ form.non_field_errors }}

                    <!-- Username -->
                    <div>
                        <label for="{{ form.username.id_for_label }}"
                               class="block text-sm font-medium text-gray-700">
                            Usuário
                        </label>
                        <div class="mt-1">
                            <input
                                type="text" name="{{ form.username.name }}"
                                id="{{ form.username.id_for_label }}"
                                value="{{ form.username.value|default_if_none:'' }}"
                                class="appearance-none block w-full
                                       px-3 py-2 border border-gray-300
                                       rounded-md shadow-sm placeholder-gray-400
                                       focus:outline-none focus:ring-2 focus:ring-blue-500 
                                       focus:border-blue-500 sm:text-sm"
                            required>
                        </div>
                        {% for error in form.username.errors %}
                            <p class="text-sm text-red-600 mt-1">{{ error }}</p>
                        {% endfor %}
                    </div>

                    <!-- Email -->
                    <div>
                        <label for="{{ form.email.id_for_label }}"
                               class="block text-sm font-medium text-gray-700">
                            Email
                        </label>
                        <div class="mt-1">
                            <input
                                type="email" name="{{ form.email.name }}"
                                id="{{ form.email.id_for_label }}"
                                value="{{ form.email.value|default_if_none:'' }}"
                                class="appearance-none block w-full
                                       px-3 py-2 border border-gray-300
                                       rounded-md shadow-sm placeholder-gray-400
                                       focus:outline-none focus:ring-2 focus:ring-blue-500 
                                       focus:border-blue-500 sm:text-sm"
                            required>
                        </div>
                        {% for error in form.email.errors %}
                            <p class="text-sm text-red-600 mt-1">{{ error }}</p>
                        {% endfor %}
                    </div>

                    <!-- Password 1 -->
                    <div>
                        <label for="{{ form.password1.id_for_label }}"
                               class="block text-sm font-medium text-gray-700">
                            Senha
                        </label>
                        <div class="mt-1">
                            <input
                                type="password"
                                name="{{ form.password1.name }}"
                                id="{{ form.password1.id_for_label }}"
                                class="appearance-none block w-full px-3 py-2
                                       border border-gray-300 rounded-md shadow-sm 
                                       placeholder-gray-400 focus:outline-none
                                       focus:ring-2 focus:ring-blue-500 
                                       focus:border-blue-500 sm:text-sm"
                            required>
                        </div>
                        {% for error in form.password1.errors %}
                            <p class="text-sm text-red-600 mt-1">{{ error }}</p>
                        {% endfor %}
                    </div>

                    <!-- Password 2 -->
                    <div>
                        <label for="{{ form.password2.id_for_label }}"
                               class="block text-sm font-medium text-gray-700">
                            Confirmar Senha
                        </label>
                        <div class="mt-1">
                            <input
                                type="password"
                                name="{{ form.password2.name }}"
                                id="{{ form.password2.id_for_label }}"
                                class="appearance-none block w-full px-3 py-2
                                       border border-gray-300 rounded-md shadow-sm 
                                       placeholder-gray-400 focus:outline-none
                                       focus:ring-2 focus:ring-blue-500 
                                       focus:border-blue-500 sm:text-sm"
                            required>
                        </div>
                        {% for error in form.password2.errors %}
                            <p class="text-sm text-red-600 mt-1">{{ error }}</p>
                        {% endfor %}
                    </div>

                    <!-- Submit -->
                    <div>
                        <button type="submit"
                            class="w-full flex justify-center py-2 px-4 border
                                   border-transparent rounded-md shadow-sm 
                                   text-sm font-medium text-white bg-blue-600
                                   hover:bg-blue-700 focus:outline-none focus:ring-2
                                   focus:ring-offset-2 focus:ring-blue-500">
                            Criar Conta
                        </button>
                    </div>

                </form>

                <!-- Divider -->
                <div class="mt-6 relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="bg-white px-2 text-gray-500">ou</span>
                    </div>
                </div>

                <!-- Footer -->
                <p class="mt-6 text-center text-sm text-gray-600">
                    Já tem uma conta?
                    <a href="/" class="font-medium text-blue-600 hover:text-blue-700">
                        Fazer login
                    </a>
                </p>

            </div>

    </main>
{% endblock %}
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```html
<!-- Form -->
<form method="post" action="" class="space-y-6">
    {% csrf_token %}

    {{ form.non_field_errors }}

</form>
```

 - `{{ form.non_field_errors }}`
   - Exibe erros de validação do formulário que *não pertencem a um campo específico*.
   - **O que é form.non_field_errors?**
     - É uma propriedade de um Django Form.
     - Retorna erros que aconteceram na validação do formulário como um todo.
   - **De onde isso vem?**
     - Isso vem do Django Forms, mais especificamente da classe:
       - *django.forms.Form*
       - *django.forms.ModelForm*
   - **Internamente, o Django mantém dois tipos de erros:**
     - **Erros por campo:**
       - Ex.: senha muito curta, email inválido.
       - Acessados com: `form.field.errors`
     - **Erros gerais (non-field errors) ← este caso:**
       - Ex.: senha1 ≠ senha2;
       - Ex.: usuário já existe;
       - Ex.: erro de autenticação;
       - Acessados com: `form.non_field_errors`










---

<div id="users-home-html"></div>

## `home.html`

> O template `home.html` será a primeira página a ser exibida assim que o usuário fizer login no sistema.

[home.html](users/templates/pages/home.html)
```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <div class="flex h-screen bg-gray-100">

        <!-- 🧱 Sidebar -->
        <aside class="w-64 bg-gray-900 text-white flex flex-col justify-between">

            <!-- Workspace Button -->
            <div class="p-2 border-b border-gray-700">
                <a class="flex items-center justify-between p-2 hover:bg-gray-800 rounded"
                    href="{% url 'workspace_home' %}">
                    Workspace
                </a>
            </div>

            <!-- Logout -->
            <div class="p-4 border-t border-gray-700">
                <a href="{% url 'logout' %}"
                   class="block text-center text-red-400 hover:text-red-300">
                   Sair
                </a>
            </div>

        </aside>

        <!-- 💼 Área principal do Home -->
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










---

<div id="users-adapters-py"></div>

## `adapters.py`

Este arquivo define **adapters personalizados do Django Allauth** usados para impedir que o Allauth adicione mensagens automáticas (via django.contrib.messages) durante fluxos de login, cadastro e autenticação social, deixando o controle das mensagens totalmente sob responsabilidade da aplicação.

[adapter.py](users/adapter.py)
```python
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoMessageAccountAdapter(DefaultAccountAdapter):
    """
    Adapter para suprimir mensagens que o allauth adicionaria ao sistema
    de messages.

    Aqui fazemos nada no add_message — assim o allauth não adiciona
    mensagens.
    """
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return


class NoMessageSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Mesmo para socialaccount, caso mensagens venham de lá."""
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return
```










---

<div id="users-forms-py"></div>

## `forms.py`

> O arquivo [users/forms.py](users/forms.py) define um formulário personalizado para criação de usuários, estendendo o `UserCreationForm` do Django.

[users/forms.py](users/forms.py)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
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

    # 🚫 Impede e-mails duplicados
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
```

 - `from django import forms`
   - Esse módulo fornece:
     - forms.Form;
     - forms.ModelForm;
     - validações (ValidationError);
     - campos de formulário (CharField, EmailField, etc.).
   - No seu código, ele é usado principalmente para:
     - lançar erros personalizados (forms.ValidationError);
     - trabalhar com validações de formulário.
 - `from django.contrib.auth.forms import UserCreationForm`
   - Importa o `UserCreationForm`, que é um formulário pronto do Django para criação de usuários.
   - Esse formulário já vem com:
     - campos username, password1 e password2;
     - validação automática de senha;
     - verificação se as duas senhas coincidem.
   - No seu código, você herda essa classe para:
     - reaproveitar toda a lógica pronta;
     - adicionar o campo email;
     - personalizar mensagens de erro e rótulos.
 - `from django.contrib.auth.models import User`
   - Importa o modelo `User` padrão do Django.
   - Esse modelo representa a tabela de usuários no banco de dados.
   - Ele é usado para:
     - dizer ao formulário qual modelo será usado (model = User);
     - verificar se já existe um usuário com o mesmo e-mail (User.objects.filter(...)).

```python
fields = ["username", "email", "password1", "password2"]
```

 - Essa linha define quais campos do formulário serão exibidos e processados durante o cadastro do usuário.
 - `fields = ["username", "email", "password1", "password2"]`
   - `fields` é uma configuração da classe Meta do formulário.
   - Ela diz ao Django quais campos devem fazer parte do formulário e em qual ordem.
 - **NOTE:** Essa linha controla o que aparece no formulário de cadastro e o que o Django vai validar e salvar, reutilizando a lógica pronta do UserCreationForm.

```python
labels = {
    "username": "Usuário",
    "email": "Email",
    "password1": "Senha",
    "password2": "Confirmar Senha",
}
```

 - Esse bloco é tipo um mapeamento de labels para os campos do formulário.
 - **Em resumo:** Esse bloco existe apenas para melhorar a experiência do usuário, deixando os textos dos campos claros, em português e alinhados com a interface do seu sistema.

```python
error_messages = {
    "username": {
        "unique": "Já existe um usuário com este nome.",
        "required": "O campo Usuário é obrigatório.",
    },
    "password2": {
        "password_mismatch": "As senhas não correspondem.",
    },
}
```

 - Esse bloco define mensagens de erro personalizadas para validações do formulário, substituindo as mensagens padrão do Django.
 - `unique`
   - Substitui a mensagem padrão exibida quando:
     - O valor de username já existe no banco de dados.
   - Esse erro vem da validação de unicidade do model *"User"*.
 - `required`
   - Substitui a mensagem padrão exibida quando:
     - O campo username é enviado vazio.
   - Essa validação ocorre antes mesmo de salvar no banco.
 - `password_mismatch`
   - Substitui a mensagem padrão exibida quando:
     - password1 e password2 são diferentes.
   - Essa validação é feita pelo *"UserCreationForm"*.

```python
# 🚫 Impede e-mails duplicados
def clean_email(self):
    email = self.cleaned_data.get("email")
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError("Este e-mail já está cadastrado.")
    return email
```

 - Essa função cria uma validação personalizada do formulário para impedir que dois usuários se cadastrem com o mesmo e-mail.
 - `email = self.cleaned_data.get("email")`
   - `self.cleaned_data` é um dicionário criado pelo Django após as validações básicas (required, formato, etc).
   - Aqui você:
     - Obtém o valor do campo email já limpo e validado.
     - Usa `.get("email")` para evitar erro caso o campo não exista.
 - `if User.objects.filter(email=email).exists():`
   - Consulta o banco de dados.
   - Verifica se já existe algum usuário com esse e-mail.
   - `exists()` é eficiente porque:
     - Não carrega o objeto inteiro.
     - Apenas verifica se há pelo menos um registro.
 - `raise forms.ValidationError("Este e-mail já está cadastrado.")`
   - Interrompe a validação do formulário.
   - Associa essa mensagem de erro diretamente ao campo email.
   - Esse erro será exibido no template através de:
     - `{% for error in form.email.errors %}`
 - `return email`
   - Retorna o valor do e-mail caso a validação passe.
   - O Django exige que o método `clean_<campo>` sempre retorne o valor limpo.

#### Onde esse formulário usado?

 - **Renderização manual:** Em vez de usar `{{ form }}` ou `{{ form.username }}`, o template renderiza cada campo manualmente para ter controle total sobre o HTML e CSS.
 - **`form.username.name`:** Retorna o nome do campo (ex: "username") para o atributo `name` do input.
 - **`form.username.id_for_label`:** Gera um ID único para o campo, usado para associar o label ao input.
 - **`form.username.value`:** Mantém o valor que o usuário digitou caso haja erro de validação, evitando que o usuário precise digitar tudo novamente.
 - **`form.username.errors`:** Lista de erros de validação específicos desse campo. O loop `{% for error in form.username.errors %}` exibe cada erro.
 - **Mesma lógica para todos os campos:** Email, password1 e password2 seguem o mesmo padrão.










---

<div id="users-url-py"></div>

## `url.py`

> Define as *ROTAS/URLs* para o app `users`.

[url.py](users/urls.py)
```python
from django.urls import path

from .views import create_account, home_view, login_view, logout_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(route="home/", view=home_view, name="home"),
    path(route="logout/", view=logout_view, name="logout"),
    path(route="create-account/", view=create_account, name="create-account"),
]
```










---

<div id="users-view-home_view"></div>

## `home_view()`

> A view `home_view()` protege a página inicial para acesso apenas de usuários logados.

[users/views.py](users/views.py)
```python
@login_required(login_url="/")
def home_view(request):
    return render(request, "pages/home.html")
```

 - `@login_required(login_url="/")`
   - Aplica um decorator do Django que exige que o usuário esteja autenticado.
   - Se o usuário não estiver logado, ele será redirecionado para a URL `/` (sua página de login).
   - Esse decorator intercepta a requisição antes da função ser executada.
 - `return render(request, "pages/home.html")`
   - Usa a função render para:
     - processar o template *pages/home.html*;
     - gerar um HTML final;
     - retornar uma resposta HTTP ao navegador.
   - Não envia contexto adicional, apenas renderiza o template.

---

<div id="users-view-create_account"></div>

## `create_account()`

> Essa view é responsável por **exibir o formulário de cadastro** e **criar uma nova conta de usuário** *a partir dos dados enviados pelo formulário*.

[users/views.py](users/views.py)
```python
def create_account(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "pages/create-account.html", {"form": form})

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("/")

        messages.error(request, "Corrija os erros abaixo.")
        return render(request, "pages/create-account.html", {"form": form})
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
if request.method == "GET":
    form = CustomUserCreationForm()
    return render(request, "pages/create-account.html", {"form": form})
```

 - Esse bloco trata a exibição inicial da página de cadastro.
 - `if request.method == "GET":`
   - Verifica se a requisição *HTTP* é do tipo *GET*.
   - Isso acontece quando o usuário acessa a página pela primeira vez, sem enviar dados ainda.
 - `form = CustomUserCreationForm()`
   - Cria uma instância vazia do formulário **CustomUserCreationForm**, criado em [users/forms.py](users/forms.py).
   - Nesse momento, o formulário não tem dados, apenas os campos (username, email, senha etc.).
 - `return render(request, "pages/create-account.html", {"form": form})`
   - Renderiza o template **create-account.html**.
   - Envia o formulário para o template através do contexto:
     - `"form": form` → permite usar {{ form }}, form.username, form.errors, etc. no HTML.
   - O usuário vê a página com o formulário pronto para preenchimento.

```python
elif request.method == "POST":
    form = CustomUserCreationForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("/")

    messages.error(request, "Corrija os erros abaixo.")
    return render(request, "pages/create-account.html", {"form": form})
```

 - **Esse bloco trata o envio do formulário de cadastro e a criação do usuário.**
 - `elif request.method == "POST":`
   - Verifica se a requisição HTTP é do tipo POST.
   - Isso acontece quando o usuário envia o formulário (clica em “Criar Conta”).
 - `form = CustomUserCreationForm(request.POST)`
   - Cria uma instância do formulário *CustomUserCreationForm*.
   - Passa *request.POST*, que contém todos os dados enviados pelo formulário (username, email, senhas).
   - A partir daqui, o formulário está preenchido com os dados do usuário.
 - `if form.is_valid():`
   - Executa todas as validações do formulário, incluindo:
     - Validações padrão do Django (UserCreationForm);
     - Validações definidas por você (ex: clean_email);
     - Regras como campos obrigatórios, senhas iguais, usuário único etc.
   - **NOTE:** Retorna *True* somente se não houver erros.
 - `form.save()`
   - Salva o novo usuário no banco de dados.
   - Internamente:
     - Cria o objeto User;
     - Criptografa a senha corretamente;
     - Persiste o usuário no banco.
 - `messages.success(request, "Conta criada com sucesso! Faça login.")`
   - Adiciona uma mensagem de sucesso ao sistema de mensagens do Django.
   - Essa mensagem pode ser exibida no template usando messages.
 - `return redirect("/")`
   - Redireciona o usuário para a rota `/` (normalmente a página de login).
   - Evita reenvio do formulário caso o usuário recarregue a página.
   - Finaliza a requisição após o cadastro bem-sucedido.

---

<div id="users-view-login_view"></div>

## `login_view()`

> Essa view é responsável por **autenticar o usuário**, processando o login e controlando o acesso à aplicação.

[users/views.py](users/views.py)
```python
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "pages/index.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(request, "Usuário ou senha inválidos.")
        return render(request, "pages/index.html")
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
if request.user.is_authenticated:
    return redirect("home")
```

 - **Esse bloco verifica se o usuário já está logado para evitar que ele acesse novamente a tela de login.**
 - `if request.user.is_authenticated:`
   - `request.user` → representa o usuário associado à requisição atual.
   -  `is_authenticated` → é uma propriedade do Django que retorna True se o usuário estiver autenticado (logado).
   - **NOTE:** Aqui estamos checando se o usuário já fez login.
 - `return redirect("home")`
   - Se o usuário já estiver autenticado, ele é redirecionado para a rota chamada "home".
   - Isso evita que um usuário logado veja ou utilize novamente a página de login.
   - É uma boa prática de UX e também de segurança básica.

```python
if request.method == "GET":
    return render(request, "pages/index.html")
```

 - **Esse bloco trata o acesso à página de login quando o usuário apenas abre a URL no navegador, mas ainda não está autenticado/logado.**
 - `if request.method == "GET":`
   - Verifica se a requisição HTTP é do tipo GET.
   - Uma requisição GET acontece quando o usuário:
     - Digita a URL no navegador;
     - Clica em um link;
     - Atualiza a página.
   - **NOTE:** Aqui significa: “o usuário está apenas pedindo a página, não enviando dados ainda”.
 - `return render(request, "pages/index.html")`
   - Renderiza (exibe) o template pages/index.html.
   - Esse template é a tela de login.
   - Nenhum processamento de autenticação é feito nesse momento, apenas a exibição da página.

```python
username = request.POST.get("username")
password = request.POST.get("password")
user = authenticate(request, username=username, password=password)
```

 - **Esse bloco coleta os dados enviados pelo formulário de login e tenta autenticar o usuário no Django.**
 - `username = request.POST.get("username")`
   - Acessa os dados enviados no formulário via método POST.
   - Busca o valor do campo chamado "username".
   - Esse nome vem do atributo *name="username"* do `<input>` no HTML.
   - O valor é armazenado na variável *username*.
 - `password = request.POST.get("password")`
   - Também acessa os dados enviados via POST.
   - Busca o valor do campo "password".
   - Esse valor é a senha digitada pelo usuário no formulário.
   - O valor é armazenado na variável *password*.
 - `user = authenticate(request, username=username, password=password)`
   - Chama o sistema de autenticação do Django.
   - O Django:
     - Procura um usuário com esse *username*;
     - Verifica se a password corresponde à senha salva (hash);
   - Se os dados estiverem corretos:
     - Retorna um objeto User
   - Se estiverem incorretos:
     - Retorna `None`
   - O resultado é armazenado na variável *"user"*.

```python
if user is not None:
    login(request, user)
    return redirect("home")
else:
    messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "pages/index.html")
```

 - **Esse bloco decide se o login será efetuado ou se uma mensagem de erro será exibida ao usuário.**
 - `if user is not None:`
   - Verifica se o processo de autenticação foi bem-sucedido.
   - *user* só será *"diferente"* de `None` quando o Django encontrou um usuário válido com a senha correta.
 - `login(request, user)`
   - Registra o usuário como logado na aplicação.
   - O Django:
     - Cria a sessão do usuário;
     - Salva o ID do usuário na sessão;
     - Passa a considerá-lo autenticado nas próximas requisições
 - `return redirect("home")`
   - Redireciona o usuário para a rota chamada *"home"*.
   - Normalmente essa rota aponta para a área *interna/protegida* da aplicação.
 - `else:`
   - Executado quando a autenticação falha (usuário ou senha inválidos).
 - `messages.error(request, "Usuário ou senha inválidos.")`
   - Adiciona uma mensagem de erro ao sistema de mensagens do Django.
   - Essa mensagem poderá ser exibida no template usando `{% if messages %}`.
 - `return render(request, "pages/index.html")`
   - Renderiza novamente a página de login.
   - Permite que o usuário veja a mensagem de erro e tente fazer login novamente.

---

<div id="users-view-logout_view"></div>

## `logout_view()`

> Essa view (função/ação) é responsável por **encerrar a sessão do usuário (logout)** e redirecioná-lo para a página inicial.

[users/views.py](users/views.py)
```python
def logout_view(request):
    logout(request)
    return redirect("/")
```

 - `logout(request)`
   - Chama a função de logout do Django.
   - O Django:
     - Remove o usuário da sessão;
     - Limpa os dados de autenticação;
     - Faz com que `request.user` volte a ser um usuário *anônimo (AnonymousUser)*.
 - `return redirect("/")`
   - Redireciona o usuário para a *rota raiz (/)*.
   - Normalmente essa rota é a página de login ou página inicial pública.


















































<!--- ( workspace/ ) --->

---

<div id="workspace-folder"></div>

## `workspace/`

> O app `workspace/` é responsável por gerenciar as **pastas** e **arquivos** do usuário.










---

<div id="workspace-workspace-home-html"></div>

## `workspace_home.html`

> O template (HTML) [`workspace_home.html`](workspace/templates/pages/workspace_home.html) é responsável pelo **gerenciamento de pastas e arquivos** do usuário.

[`workspace_home.html`](workspace/templates/pages/workspace_home.html)
```html
Em breve...
```










---

<div id="workspace-admin-py"></div>

## `admin.py`

Este arquivo configura o **Django Admin**, registrando os modelos da aplicação para que possam ser gerenciados pela interface administrativa do Django.

[admin.py](workspace/admin.py)
```python
from django.contrib import admin

from .models import File, Folder

admin.site.register(Folder)
admin.site.register(File)
```

 - `from .models import File, Folder`
   - Importa os modelos `File` e `Folder` definidos no arquivo [models.py](workspace/models.py) do mesmo app.
   - O *ponto (.)* indica importação relativa ao app atual.
 - `admin.site.register(Folder)`
   - Registra o modelo *Folder* no Django Admin.
   - A partir disso:
     - O modelo aparece no painel administrativo;
     - Pode ser criado, editado e excluído pela interface web do admin.
 - `admin.site.register(File)`
   - Registra o modelo *File* no Django Admin.
   - Permite o gerenciamento de arquivos diretamente pelo painel administrativo.










---

<div id="workspace-forms-py"></div>

## `forms.py`

Este arquivo define **formulários Django (ModelForms)** responsáveis por:

 - Validar;
 - Criar;
 - Personalizar...

a *criação de pastas* e o *upload de arquivos*, incluindo regras de validação como tamanho máximo de arquivo e tratamento automático de nomes.

---

<div id="workspace-forms-validate-file-size"></div>

## `validate_file_size() function`

> Esse *validador* garante que o arquivo enviado não ultrapasse um tamanho máximo (50 MB) permitido.

[forms.py](workspace/forms.py)
```python
def validate_file_size(value):
    max_mb = 100  # 100 MB
    if value.size > max_mb * 1024 * 1024:
        raise ValidationError(f"O arquivo não pode ser maior que {max_mb} MB.")
```

 - `max_mb = 100`
   - Define o tamanho máximo permitido em megabytes.
   - Neste caso, o limite é 100 MB.
 - `if value.size > max_mb * 1024 * 1024`
   - Verifica o tamanho real do arquivo em bytes.
   - O cálculo `1024 * 1024` converte megabytes para bytes.
   - Se o tamanho do arquivo for maior que 50 MB, a condição é satisfeita.
 - `raise ValidationError(f"O arquivo não pode ser maior que {max_mb} MB.")`
   - Lança um erro de validação do Django.
   - Esse erro:
     - Impede o envio do formulário;
     - É associado ao campo de arquivo;
     - Pode ser exibido diretamente no template como mensagem de erro .

> **📌 Na prática:**  
> Esse validador é usado em campos *"FileField"* para bloquear uploads grandes demais antes de salvar no banco ou no disco.

---

<div id="workspace-forms-folderform-class"></div>

## `FolderForm() class`

> Essa classe (formulário) é responsável por **criar** e **validar pastas**, garantindo que o nome seja informado corretamente e aplicando personalizações visuais e mensagens de erro.

[forms.py](workspace/forms.py)
```python
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
            "name": {"required": "O nome da pasta é obrigatório."},
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        # opcional: garantir unicidade no mesmo parent/owner
        if not name:
            raise ValidationError("Nome inválido.")
        return name
```

 - `model = Folder`
   - Informa que este formulário está ligado ao modelo *"Folder"*.
   - Quando o formulário for salvo, ele criará ou atualizará um objeto *"Folder"*.
 - `widgets = {}`
   - Permite personalizar o HTML gerado para os campos do formulário.
   - `"name": forms.TextInput()`
     - Define que o campo `name` será renderizado como um `<input type="text">`.
   - `attrs = {}`
     - Define atributos HTML extras para o campo.
     - `"placeholder": "Nome da pasta",`
       - Define um texto de dica exibido dentro do input quando ele está vazio.
 - `def clean_name(self):`
   - `name = self.cleaned_data.get("name", "").strip()`
     - Obtém o valor do campo name após as validações iniciais.
     - Usa *strip()* para remover espaços extras no início e no fim.
   - `if not name:`
     - Verifica se o nome ficou vazio após remover os espaços.
   - `raise ValidationError("Nome inválido.")`
     - Lança um erro de validação se o nome for inválido.
     - Impede o salvamento do formulário.
   - `return name`
     - Retorna o valor validado do campo.
     - Esse valor será usado para criar ou atualizar o objeto Folder.

---

<div id="workspace-forms-fileform-class"></div>

## `FileForm() class`

> Essa classe (formulário) é responsável por **criar** e **validar arquivos enviados pelo usuário**, aplicando validações de upload (como tamanho máximo) e definindo automaticamente o nome do arquivo quando ele não é informado.

[forms.py](workspace/forms.py)
```python
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
            "file": forms.ClearableFileInput(attrs={"class": "block w-full"}),
        }
        error_messages = {
            "file": {"required": "Selecione um arquivo para enviar."},
        }

    # adiciona validação de tamanho
    file = forms.FileField(validators=[validate_file_size])

    def clean_name(self):
        name = self.cleaned_data.get("name")
        uploaded = self.cleaned_data.get("file")
        if not name and uploaded:
            # se o usuário não informou o name,
            # preenche com o filename (sem path)
            return uploaded.name
        return name
```

 - `fields = ["name", "file"]`
   - Define quais campos do modelo File serão exibidos e processados pelo formulário.
   - `name` → Nome do arquivo (opcional).
   - `file` → O arquivo em si.
 - `file = forms.FileField(validators=[validate_file_size])`
   - Redefine explicitamente o campo file no formulário.
   - Adiciona o validador **validate_file_size()**.
   - Isso garante que:
     - O arquivo respeite o tamanho máximo definido;
     - A validação ocorra antes de salvar no banco ou no disco.
 - `def clean_name(self):`
   - `name = self.cleaned_data.get("name")`
     - Obtém o valor informado no campo name após as validações iniciais.
   - `uploaded = self.cleaned_data.get("file")`
     - Obtém o arquivo enviado pelo usuário.
   - `if not name and uploaded:`
     - Verifica se:
       - O usuário não informou um nome;
       - Mas enviou um arquivo.
   - `return uploaded.name`
     - Usa automaticamente o nome original do arquivo enviado (sem o caminho).
     - Isso garante que o campo `name` nunca fique vazio quando um arquivo existir.

---

<div id="workspace-forms-fileuploadform-class"></div>

## `FileUploadForm() class`

> Essa classe (formulário) é um formulário simplificado de upload, usado quando apenas o arquivo precisa ser enviado, sem informações adicionais.

[forms.py](workspace/forms.py)
```python
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]
```










---

<div id="workspace-models-py"></div>

## `models.py`

Este arquivo define os modelos **centrais do workspace**, responsáveis por:

 - Representar pastas e arquivos dos usuários;
 - Incluindo hierarquia de pastas;
 - Controle de ownership;
 - Upload seguro de arquivos e metadados;
   - Como data de criação e exclusão lógica.

---

<div id="workspace-models-workspace-upload-to"></div>

## `workspace_upload_to() function`

> Essa função define **onde** e **como** *os arquivos enviados serão armazenados dentro do MEDIA_ROOT*, organizando-os por usuário e pasta.

[models.py](workspace/models.py)
```python

def workspace_upload_to(instance, filename):
    """
    Constrói o path onde o arquivo será salvo dentro de MEDIA_ROOT:
    workspace/<user_id>/<folder_id_or_root>/<filename>
    """
    user_part = (
        f"user_{instance.folder.owner.id}"
        if instance.folder and instance.folder.owner
        else f"user_{instance.uploader.id}"
    )

    folder_part = f"folder_{instance.folder.id}" if instance.folder else "root"

    # Limpa o nome do arquivo por segurança básica
    safe_name = os.path.basename(filename)

    return os.path.join("workspace", user_part, folder_part, safe_name)
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
user_part = (
    f"user_{instance.folder.owner.id}"
    if instance.folder and instance.folder.owner
    else f"user_{instance.uploader.id}"
)
```

 - **Esse bloco define qual usuário será usado para organizar o caminho do arquivo, garantindo que ele fique associado ao dono correto.**
 - `f"user_{instance.folder.owner.id}"`
   - Cria uma string com o ID do dono da pasta.
   - Exemplo de resultado: *user_5*
 - `if instance.folder and instance.folder.owner`
   - Verifica duas condições:
     - O arquivo está associado a uma pasta (instance.folder);
     - Essa pasta tem um dono definido (instance.folder.owner).
   - Isso evita erros de acesso a atributos inexistentes (None).
 - `else f"user_{instance.uploader.id}"`
   - Caso o arquivo não esteja em uma pasta:
     - Usa o ID do usuário que fez o upload (uploader).
   - Garante que todo arquivo sempre tenha um usuário associado.

```python
folder_part = f"folder_{instance.folder.id}" if instance.folder else "root"

# Limpa o nome do arquivo por segurança básica
safe_name = os.path.basename(filename)

return os.path.join("workspace", user_part, folder_part, safe_name)
```

 - `folder_part = f"folder_{instance.folder.id}" if instance.folder else "root"`
   - Define a parte do caminho referente à pasta:
     - Se o arquivo estiver em uma pasta → `folder_<id>`;
     - Se não estiver em nenhuma pasta → root
 - `safe_name = os.path.basename(filename)`
   - Remove qualquer caminho do nome do arquivo.
   - Garante que apenas o nome do arquivo seja usado, evitando:
     - `Path traversal (../../)`
     - Problemas de segurança ou sobrescrita indevida.
 - `return os.path.join("workspace", user_part, folder_part, safe_name)`
   - Monta o caminho final do arquivo usando separadores corretos do sistema operacional.
   - O caminho retornado será algo como:
     - `workspace/user_3/folder_12/documento.pdf`
   - O Django salva o arquivo automaticamente dentro de:
     - `MEDIA_ROOT/workspace/user_3/folder_12/documento.pdf`

---

<div id="workspace-models-folder-class">

## `Folder() class`

> Essa classe define o modelo *Folder*, responsável por **representar pastas de usuários**, com **suporte a hierarquia (pastas dentro de pastas)**, controle de dono e metadados de criação e exclusão lógica.

[models.py](workspace/models.py)
```python
class Folder(models.Model):
    """
    Representa uma pasta do usuário. Suporta hierarquia via parent (self-FK).
    """

    name = models.CharField(_("name"), max_length=255)

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
        return self.name
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
name = models.CharField(_("name"), max_length=255)
```

 - **Essa linha define um campo de texto no modelo Django:**
 - `models.CharField()` → campo de string de tamanho fixo no banco de dados;
 - `_("name")` → rótulo legível do campo, marcado para tradução (i18n);
 - `max_length=255` → limite máximo de 255 caracteres, usado tanto no banco quanto na validação do Django

```python
owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="folders",
)
```

 - **Introdução:**
   - Esse bloco define um **relacionamento entre a pasta (Folder) e o usuário do sistema**.
   - Ele diz que cada pasta pertence a um único usuário, enquanto um usuário pode ter várias pastas.
   - É assim que o Django modela relações um-para-muitos no banco de dados.
 - **Codificação:**
   - `owner = models.ForeignKey( ... )`
     - Cria um campo chamado **owner** que representa uma chave estrangeira (Foreign Key);
     - Ou seja, uma referência a outro modelo.
   - `settings.AUTH_USER_MODEL`
     - Indica que o relacionamento é com o modelo de usuário configurado no projeto (seja o User padrão ou um customizado).
     - Isso é melhor prática em Django, pois evita acoplamento direto.
   - `on_delete=models.CASCADE`
     - Define o comportamento quando o usuário é deletado:
     - **NOTE:** Se o usuário for removido, todas as pastas dele também serão apagadas automaticamente no banco.
   - `related_name="folders"`
     - Define o nome do relacionamento reverso.
     - Permite acessar as pastas de um usuário assim:
       - `user.folders.all()`
 - **Resumo conceitual:**
   - 📁 Uma pasta pertence a um usuário;
   - 👤 Um usuário pode ter várias pastas;
   - 🧹 Deletar o usuário → deleta as pastas;
   - 🔄 Acesso reverso limpo e explícito (user.folders)

```python
parent = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    related_name="children",
)
```

 - **Introdução:**
   - Esse bloco define um **relacionamento recursivo** no modelo `Folder`.
   - Ele permite que uma pasta contenha outras pastas, criando uma estrutura hierárquica (árvore) semelhante a um sistema de arquivos real.
   - *Em outras palavras:* uma pasta pode ter uma pasta pai, e essa pasta pai pode ter várias pastas filhas.
 - **Codificação:**
   - `parent = models.ForeignKey( ... )`
     - Cria um campo chamado `parent` que será uma chave estrangeira apontando para outra instância de `Folder`.
   - `"self"`
     - Indica que o relacionamento é com o próprio modelo Folder.
     - Isso é obrigatório quando se quer criar hierarquias dentro do mesmo modelo.
   - `null=True`
     - Permite que o campo seja NULL no banco de dados.
     - Isso é necessário para pastas que ficam na raiz, ou seja, não têm pasta pai.
   - `blank=True`
     - Permite que o campo fique vazio em formulários e validações do Django.
     - Sem isso, o Django exigiria um parent sempre que uma pasta fosse criada.
   - `on_delete=models.CASCADE`
     - Define o comportamento ao deletar a pasta pai:
       - Se uma pasta for removida, todas as suas subpastas também serão removidas.
   - `related_name="children"`
     - Define o nome do relacionamento reverso.
     - Permite acessar as subpastas assim:
       - `folder.children.all()`
 - **Resumo conceitual:**
   - 🌳 Estrutura em árvore;
   - 📁 Pasta pode ter pai ou ser raiz;
   - 👶 Uma pasta pode ter várias filhas;
   - 🧹 Deletar uma pasta remove toda a subárvore;
   - 🔄 Navegação fácil: folder.children

```python
created_at = models.DateTimeField(auto_now_add=True)
is_deleted = models.BooleanField(default=False)
deleted_at = models.DateTimeField(null=True, blank=True)
```

 - **Introdução:**
   - Esse bloco implementa **controle de tempo de criação** e **soft delete** no modelo.
   - Em vez de apagar registros definitivamente do banco, o sistema pode marcá-los como deletados, preservando histórico, integridade e possibilidade de auditoria ou restauração.
 - **Codificação:**
   - `created_at = models.DateTimeField(auto_now_add=True)`
     - Cria um campo de data e hora que é preenchido automaticamente no momento da criação do registro.
     - Depois de salvo, esse valor nunca é alterado pelo Django.
   - `is_deleted = models.BooleanField(default=False)`
     - Campo booleano que indica se o registro está logicamente deletado:
       - *False* → ativo;
       - *True* → considerado removido pelo sistema.
     - **NOTE:** O registro continua no banco, mas pode ser *ignorado nas consultas (Soft Delete)*.
   - `deleted_at = models.DateTimeField(null=True, blank=True)`
     - Armazena quando o *soft delete* ocorreu:
       - null=True → pode ser NULL no banco;
       - blank=True → opcional em formulários
     - Normalmente é preenchido somente quando *is_deleted* vira *True*.
 - **Resumo conceitual:**
   - 🕒 created_at → quando o objeto foi criado;
   - 🚫 is_deleted → flag de exclusão lógica;
   - 🧾 deleted_at → registro do momento da exclusão;
   - ✅ Mantém histórico e evita perda definitiva de dados

```python
class Meta:
    ordering = ["-created_at"]
    verbose_name = _("Folder")
    verbose_name_plural = _("Folders")
```

 - **Introdução:**
   - O bloco (classe) `Meta` define configurações adicionais (metadados) do modelo *Folder*.
   - Ele não cria campos no banco, mas controla como o Django trata, ordena e exibe o modelo internamente (admin, queries padrão, mensagens, etc.).
 - **Codificação:**
   - `ordering = ["-created_at"]`
     - Define a ordenação padrão das consultas desse modelo.
     - `-created_at` → ordem decrescente.
     - Pastas mais recentes aparecem primeiro.
   - `verbose_name = _("Folder")`
     - Define o nome legível no singular do modelo, usado principalmente no Django Admin e mensagens.
     - O `_()` marca o texto para tradução (i18n).
   - `verbose_name_plural = _("Folders")`
     - Define o nome legível no plural do modelo.
     - Evita plurais automáticos incorretos e mantém suporte a tradução.
 - **Resumo conceitual:**
   - 📦 Meta → comportamento do modelo, não estrutura;
   - 🔽 ordering → ordenação padrão global;
   - 🏷️ verbose_name → nome amigável (singular);
   - 🏷️ verbose_name_plural → nome amigável (plural);
   - 🌍 Suporte a internacionalização

```python
def __str__(self):
    return self.name
```

 - **Introdução:**
   - Esse bloco define como uma instância do modelo será representada como texto.
 - **Codificação:**
   - `def __str__(self):`
     - Define o método especial `__str__`, que controla a representação em string do objeto quando ele é convertido para texto.
   - `return self.name`
     - Retorna o valor do campo `name` como a representação textual da instância.
     - Assim, uma pasta será exibida pelo seu nome, o que é intuitivo e legível.

---

<div id="workspace-models-file-class"></div>

## `File() class`

> A classe **File()** representa um arquivo enviado pelo usuário, definindo como ele é armazenado, organizado em pastas e associado a quem fez o upload, além de controlar seu ciclo básico de existência no sistema.

[models.py](workspace/models.py)
```python
class File(models.Model):
    name = models.CharField(_("name"), max_length=255)

    file = models.FileField(_("file"), upload_to=workspace_upload_to)

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
        return self.name
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
file = models.FileField(_("file"), upload_to=workspace_upload_to)
```

 - **Introdução:**
   - Esse bloco define o campo responsável por armazenar o arquivo físico enviado pelo usuário.
   - Ele conecta o modelo *File* a um arquivo real no sistema de arquivos (ou storage configurado), controlando onde o arquivo será salvo e como ele será referenciado no banco de dados.
 - **Codificação:**
   - `file = models.FileField()`
     - Cria um campo do tipo `FileField`, usado pelo Django para lidar com upload, armazenamento e acesso a arquivos.
   - `_("file")`
     - Define o nome legível do campo, marcado para tradução (i18n).
     - Esse rótulo aparece em formulários, validações e no Django Admin.
   - `upload_to=workspace_upload_to`
     - Define (chama) uma função customizada que determina o caminho onde o arquivo será salvo dentro do `MEDIA_ROOT`.
     - No momento do upload, o Django chama essa função passando:
       - a instância do modelo (instance);
       - o nome original do arquivo (filename).
     - A função retorna um path dinâmico, por exemplo:
       - `workspace/user_3/folder_10/document.pdf`
     - Isso permite:
       - organização por usuário;
       - organização por pasta;
       - evitar colisões;
       - refletir a hierarquia lógica no storage.
 - **Resumo conceitual:**
   - 📄 Campo responsável pelo arquivo físico;
   - 📂 Salvo automaticamente em MEDIA_ROOT;
   - 🧠 Caminho definido dinamicamente via função;
   - 🌍 Suporte a tradução no rótulo;
   - 🔗 Integra modelo ↔ sistema de arquivos.

```python
folder = models.ForeignKey(
    Folder,
    on_delete=models.CASCADE,
    related_name="files",
    null=True,
    blank=True,
)
```

 - **Introdução:**
   - Esse bloco define o relacionamento entre o *arquivo (File)* e a *pasta (Folder)*.
   - Ele permite que um arquivo esteja dentro de uma pasta específica ou na raiz, reproduzindo o comportamento clássico de um sistema de arquivos.
   - Em termos de modelagem:
     - Uma pasta pode conter vários arquivos;
     - Um arquivo pertence a no máximo uma pasta.
 - **Codificação:**
   - `folder = models.ForeignKey( ... )`
     - Cria um campo chamado folder que representa uma chave estrangeira para uma pasta.
   - `Folder`
     - Indica que o relacionamento é com o modelo Folder.
     - Cada arquivo aponta diretamente para uma pasta existente.
   - `on_delete=models.CASCADE`
     - Define o comportamento quando a pasta é deletada:
       - Todos os arquivos dentro dessa pasta também são removidos do banco.
   - `related_name="files"`
     - Define o nome do relacionamento reverso.
     - Permite acessar os arquivos de uma pasta assim:
       - `folder.files.all()`
   - `null=True`
     - Permite que o campo seja NULL no banco de dados.
     - Isso representa arquivos que estão na raiz, sem pasta associada.
   - `blank=True`
     - Permite que o campo seja opcional em formulários e validações.
     - Sem isso, o Django exigiria sempre uma pasta ao criar um arquivo.
 - **Resumo conceitual:**
   - 📁 Pasta → muitos arquivos;
   - 📄 Arquivo → zero ou uma pasta;
   - 🌱 Suporte a arquivos na raiz;
   - 🧹 Cascade mantém consistência;
   - 🔄 Acesso reverso simples (folder.files).

```python
uploader = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="uploaded_files",
)
```

 - **Introdução:**
   - Esse bloco define quem enviou o arquivo para o sistema.
   - Ele registra explicitamente o usuário responsável pelo upload, o que é fundamental para:
     - auditoria;
     - controle de acesso;
     - permissões;
     - histórico de ações.
   - **NOTE:** Mesmo que o arquivo esteja dentro de uma pasta de outro contexto, o autor do upload continua identificado.
 - **Codificação:**
   - `uploader = models.ForeignKey( ... )`
     - Cria um campo chamado `uploader` que representa uma chave estrangeira.
   - `settings.AUTH_USER_MODEL`
     - Indica que o relacionamento é com o modelo de usuário configurado no projeto.
     - Isso garante compatibilidade com usuários customizados.
   - `on_delete=models.CASCADE`
     - Define o comportamento ao deletar o usuário:
       - Se o usuário for removido, todos os arquivos enviados por ele também serão removidos.
   - `related_name="uploaded_files"`
     - Define o nome do relacionamento reverso.
     - Permite acessar todos os arquivos enviados por um usuário assim:
       - `user.uploaded_files.all()`
 - **Resumo conceitual:**
   - 👤 Identifica o autor do upload;
   - 📄 Um usuário → muitos arquivos enviados;
   - 🧹 Cascade mantém integridade;
   - 🔄 Acesso reverso explícito (uploaded_files);
   - 🔍 Base para permissões e auditoria










---

<div id="workspace-url-py"></div>

## `url.py`

> Define as *ROTAS/URLs* para o app `workspace`

[url.py](workspace/urls.py)
```python
from django.urls import path

from . import views

urlpatterns = [
    path(route="workspace", view=views.workspace_home, name="workspace_home"),
    path(route="create-folder/", view=views.create_folder, name="create_folder"),
    path(route="upload-file/", view=views.upload_file, name="upload_file"),
    path(route="delete-folder/<int:folder_id>/", view=views.delete_folder, name="delete_folder"),
    path(route="delete-file/<int:file_id>/", view=views.delete_file, name="delete_file"),
    path(route="rename-folder/<int:folder_id>/", view=views.rename_folder, name="rename_folder"),
    path(route="rename-file/<int:file_id>/", view=views.rename_file, name="rename_file"),
    path(route="move-item/", view=views.move_item, name="move_item"),
]
```










---

<div id="workspace-validators-py"></div>

## `validators.py`

> Esse arquivo centraliza as regras de validação de arquivos enviados, garantindo que apenas formatos permitidos e tamanhos aceitáveis sejam aceitos pelo sistema antes do armazenamento.

[validators.py](workspace/validators.py)
```python
import os

from django.core.exceptions import ValidationError

MAX_FILE_MB = 100
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".xlsm",
    ".csv"
}
ALLOWED_FORMATTED = ", ".join(ext.upper() for ext in ALLOWED_EXTENSIONS)


def validate_file_type(uploaded_file):
    """Valida o tipo de arquivo pela extensão."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        # Quebra de linha para evitar E501
        msg = (
            f"Arquivo inválido: '{uploaded_file.name}'. "
            f"O formato '{ext}' não é permitido. "
            f"Apenas {ALLOWED_FORMATTED} são aceitos."
        )
        raise ValidationError(msg)


def validate_file_size(uploaded_file):
    """Valida o tamanho do arquivo."""
    if uploaded_file.size > MAX_FILE_BYTES:
        # Outra quebra de linha para evitar E501
        msg = (
            f"O arquivo '{uploaded_file.name}' excede o limite "
            f"de {MAX_FILE_MB}MB."
        )
        raise ValidationError(msg)


def validate_file(uploaded_file):
    """
    Validação completa: tipo + tamanho.
    """
    validate_file_type(uploaded_file)
    validate_file_size(uploaded_file)
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
ALLOWED_FORMATTED = ", ".join(ext.upper() for ext in ALLOWED_EXTENSIONS)
```

 - **Introdução:**
   - Essa linha cria uma string formatada e legível com as extensões de arquivo permitidas, geralmente para exibição ao usuário (mensagens de erro, validações, help text em formulários).
   - Ela transforma uma coleção de extensões técnicas em um texto amigável.
 - **Codificação:**
   - `ALLOWED_EXTENSIONS`
     - Uma coleção (lista, set ou tupla) contendo extensões permitidas, por exemplo:
       - `{"pdf", "txt", "docx"}`
   - `for ext in ALLOWED_EXTENSIONS`
     - Itera por cada extensão permitida.
   - `ext.upper()`
     - Converte a extensão para letras maiúsculas, apenas para apresentação visual (não muda a regra de validação).
   - `", ".join(...)`
     - Junta todas as extensões em uma única string, separadas por vírgula e espaço.
   - `📌 Resultado final:`
     - `"PDF, TXT, DOCX"`
 - **Resumo conceitual:**
   - 🧾 Cria texto amigável para o usuário;
   - 🔤 Apenas formatação (não afeta validação);
   - ♻️ Sempre sincronizado com ALLOWED_EXTENSIONS;
   - ✅ Boa prática para mensagens de erro e UI

---

<div id="workspace-validate-file-type"></div>

#### `validate_file_type()`

 - Esse bloco define uma função de validação personalizada usada pelo Django para verificar se o arquivo enviado tem uma extensão permitida.
 - Ela é normalmente associada a um FileField e é executada no momento do upload, antes de salvar o arquivo.
 - O objetivo é:
   - bloquear formatos não suportados;
   - evitar processamento desnecessário;
   - fornecer uma mensagem de erro clara ao usuário.

[validators.py](workspace/validators.py)
```python
def validate_file_type(uploaded_file):
    """Valida o tipo de arquivo pela extensão."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        # Quebra de linha para evitar E501
        msg = (
            f"Arquivo inválido: '{uploaded_file.name}'. "
            f"O formato '{ext}' não é permitido. "
            f"Apenas {ALLOWED_FORMATTED} são aceitos."
        )
        raise ValidationError(msg)
```

 - `ext = os.path.splitext(uploaded_file.name)[1].lower()`
   - `uploaded_file.name` → nome original do arquivo.
   - `os.path.splitext(...)` → separa nome e extensão;
   - `[1]` → pega apenas a extensão (ex: .pdf);
   - `.lower()` → normaliza para minúsculas.
 - `if ext not in ALLOWED_EXTENSIONS:`
   - Verifica se a extensão extraída não está na lista/conjunto de extensões permitidas.
 - `raise ValidationError(msg)`
   - Lança uma exceção do Django:
     - interrompe o processo de upload;
     - exibe a mensagem ao usuário;
     - impede o salvamento do arquivo.

---

<div id="workspace-validate-file-size"></div>

#### `validate_file_size()`

 - Esse bloco define uma validação personalizada de tamanho de arquivo.
 - Ela impede que usuários façam upload de arquivos maiores que o limite permitido, protegendo:
   - desempenho do servidor;
   - consumo de storage;
   - tempo de processamento (especialmente importante em RAG);
   - A validação ocorre antes do arquivo ser salvo.

[validators.py](workspace/validators.py)
```python
def validate_file_size(uploaded_file):
    """Valida o tamanho do arquivo."""
    if uploaded_file.size > MAX_FILE_BYTES:
        # Outra quebra de linha para evitar E501
        msg = (
            f"O arquivo '{uploaded_file.name}' excede o limite "
            f"de {MAX_FILE_MB}MB."
        )
        raise ValidationError(msg)
```

 - `if uploaded_file.size > MAX_FILE_BYTES:`
   - A condição verifica se o arquivo excede o tamanho permitido.
   - `uploaded_file.size` → tamanho do arquivo em bytes.
   - `MAX_FILE_BYTES` → limite máximo permitido (ex: 10 * 1024 * 1024)
 - `raise ValidationError(msg)`
   - Lança uma exceção de validação:
     - interrompe o upload;
     - impede o salvamento;
     - exibe o erro ao usuário.

---

<div id="workspace-validate-file"></div>

#### `validate_file()`

 - Esse bloco define uma validação composta para arquivos.
 - Em vez de aplicar várias validações separadamente no modelo ou formulário, ele centraliza todas as regras de validação em uma única função, garantindo que o arquivo só será aceito se todas as regras forem satisfeitas.
 - Isso melhora:
   - organização do código;
   - reutilização;
   - manutenção futura.

[validators.py](workspace/validators.py)
```python
def validate_file(uploaded_file):
    """
    Validação completa: tipo + tamanho.
    """
    validate_file_type(uploaded_file)
    validate_file_size(uploaded_file)
```










---

<div id="workspace-view-workspace-home">

### `workspace_home()`

> A view **workspace_home()** é a responsável por exibir o explorador de arquivos do usuário, *mostrando pastas*, *arquivos* e o *caminho de navegação (breadcrumbs)*, tanto na raiz quanto dentro de uma pasta específica.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def workspace_home(request):

    folder_id = request.GET.get("folder")

    # 📁 1. Se o usuário clicou em alguma pasta
    if folder_id:

        # Busca a pasta atual
        current_folder = get_object_or_404(
            Folder, id=folder_id, owner=request.user
        )

        # Busca subpastas
        folders = Folder.objects.filter(
            parent=current_folder, is_deleted=False
        )

        # Busca arquivos da pasta
        files = File.objects.filter(
            folder=current_folder, is_deleted=False
        )

        # Breadcrumbs (caminho completo)
        breadcrumbs = []
        temp = current_folder
        while temp:
            breadcrumbs.append(temp)
            temp = temp.parent
        breadcrumbs.reverse()

    else:
        # 📁 2. Estamos no nível raiz
        current_folder = None

        # Pastas da raiz
        folders = Folder.objects.filter(
            owner=request.user, parent__isnull=True, is_deleted=False
        )

        # Arquivos da raiz
        files = File.objects.filter(
            uploader=request.user, folder__isnull=True, is_deleted=False
        )

        breadcrumbs = []  # Raiz não tem caminho

    # Contexto do template
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
   - Ela tenta ler da URL o parâmetro chamado `folder`.
   - Exemplo de URL:
     - `/workspace?folder=5`
   - Resultado:
     - `folder_id == "5"` (string)
     - Se não existir `?folder=...`, o valor será `None`
   - **NOTE:** Essa linha decide se o usuário está navegando na raiz ou dentro de uma pasta.
 - **Codificação:**
   - `folder_id = request.GET.get("folder")`
     - `request.GET`
       - O **request.GET** é um dicionário especial do Django (QueryDict) que contém todos os parâmetros enviados pela URL (query string).
       - Exemplo de URL: `/workspace?folder=12&page=2`
       - Conteúdo de request.GET:
         - `{"folder": "12", "page": "2"}`
       - **NOTE:** Ele só lê dados do método GET (nada de POST aqui).
     - `.get("folder")`
       - O **.get()** é um método de dicionários (e do QueryDict) que tenta pegar um valor pela chave.
       - Significa:
         - “Pegue o valor associado à chave "folder" se ela existir.”
         - Se "folder" existir → retorna o valor (como string);
         - Se "folder" não existir → retorna None;
         - Não lança erro

```python
if folder_id:
    ...
else:
    ...
```

 - **Quando o if folder_id é usado?**
   - Quando existe `?folder=<id>` na URL;
   - Significa: o usuário clicou em uma pasta;
   - O sistema deve mostrar conteúdo dessa pasta
 - **Quando o else é usado?**
   - Quando não existe o parâmetro folder;
   - Significa: *o usuário está na raiz*;
   - O sistema deve mostrar pastas e arquivos soltos;
   - **NOTE:** Esse *if/else* define o nível da navegação.

```python
# Buscar a pasta atual
current_folder = get_object_or_404(
    Folder, id=folder_id, owner=request.user
)
```

 - **Introdução:**
   - Esse bloco identifica qual pasta o usuário está tentando acessar, garantindo:
     - que ela existe;
     - que ela pertence ao usuário logado.
 - **Codificação:**
   - `current_folder = get_object_or_404()`
     - *get_object_or_404()* é uma função utilitária do Django usada para buscar um único objeto no banco de dados e retornar automaticamente um erro 404 se ele (o objeto) não existir ou não atender aos filtros informados.
     - Ela é muito usada em *views* porque simplifica código e aumenta a segurança.
     - Ela executa o equivalente a:
       - Faz uma consulta no banco;
       - Se encontrar exatamente um objeto → retorna esse objeto;
       - Se não encontrar nenhum → lança `Http404`;
       - Se os filtros não baterem (ex: objeto de outro usuário) → também lança `Http404`.
       - **NOTE:** Ou seja: 👉 o usuário só vê o objeto se ele realmente puder acessá-lo.
     - `Folder, id=folder_id, owner=request.user`
       - `Folder` → Modelo onde a busca será feita.
       - `id=folder_id` → Filtra pela pasta cujo ID veio da URL.
       - `owner=request.user` → Garante que a pasta pertence ao usuário autenticado (segurança):
         - Se qualquer condição falhar → 404.

```python
# Busca subpastas
folders = Folder.objects.filter(
    parent=current_folder, is_deleted=False
)
```

 - **Introdução:**
   - Esse bloco carrega as pastas filhas da pasta atual.
 - **Codificação:**
   - `folders = Folder.objects.filter()`
     - `Folder.`
       - *Folder* é o modelo Django, que representa a tabela folder no banco de dados.
     - `objects.`
       - É o manager padrão do Django.
       - Ele é a “porta de entrada” para fazer consultas no banco relacionadas a esse modelo.
       - Pense como: **“Quero falar com o banco sobre Folder”.**
     - `filter()`
       - É um método de consulta que:
         - aplica condições;
         - retorna zero, um ou vários objetos;
         - nunca lança erro se não encontrar nada.
       - **NOTE:** O retorno é sempre um *QuerySet*.
       - No nosso caso, significa:
         - **“Busque todas as pastas cujo pai é *"current_folder"* e que não estejam deletadas”.**
     - `parent=current_folder` → Busca apenas pastas cujo pai é a pasta atual.
     - `is_deleted=False` → Exclui pastas marcadas como deletadas (soft delete).

```python
# Busca arquivos da pasta
files = File.objects.filter(
    folder=current_folder, is_deleted=False
)
```

 - **Introdução:**
   - Esse bloco carrega os arquivos contidos na pasta atual.
 - **Codificação:**
   - `files = File.objects.filter()`
     - Inicia uma consulta no modelo `File`.
     - `folder=current_folder` → Seleciona apenas arquivos que pertencem à pasta atual.
     - `is_deleted=False` → Ignora arquivos deletados logicamente (soft delete).

```python
# Breadcrumbs (caminho completo)
breadcrumbs = []
temp = current_folder
while temp:
    breadcrumbs.append(temp)
    temp = temp.parent
breadcrumbs.reverse()
```

 - **Introdução:**
   - Esse bloco constrói o caminho hierárquico completo da pasta atual até a raiz.
 - **Codificação:**
   - `breadcrumbs = []`
     - Lista vazia para armazenar o caminho.
   - `temp = current_folder`
     - Variável temporária para navegar pela hierarquia.
   - `while temp:`
     - Loop enquanto existir uma pasta (até chegar na raiz).
   - `breadcrumbs.append(temp)`
     - Adiciona a pasta atual ao caminho.
   - `temp = temp.parent`
     - Sobe um nível (vai para a pasta pai).
   - `breadcrumbs.reverse()`
     - Inverte a lista para ficar: **Raiz → ... → Pasta atual**

```python
else:
    # 📁 2. Estamos no nível raiz
    current_folder = None
```

 - **Introdução:**
   - Esse bloco indica explicitamente que não há pasta selecionada.
 - **Codificação:**
   - `current_folder = None`
     - Marca que o usuário está no nível raiz.
     - Usado pelo template para ajustar comportamento visual.

```python
folders = Folder.objects.filter(
    owner=request.user, parent__isnull=True, is_deleted=False
)
```

 - **Introdução:**
   - Esse bloco carrega pastas que não têm pai, ou seja, pastas da raiz.
 - **Codificação:**
   - `owner=request.user`
     - Somente pastas do usuário logado.
   - `parent__isnull=True`
     - Seleciona apenas pastas sem pai (nível raiz).
   - `is_deleted=False`
     - Ignora pastas deletadas (soft delete).

```python
# Arquivos da raiz
files = File.objects.filter(
    uploader=request.user, folder__isnull=True, is_deleted=False
)
```

 - **Introdução:**
   - Esse bloco carrega arquivos soltos, que não pertencem a nenhuma pasta.
 - **Codificação:**
   - `uploader=request.user`
     - Somente arquivos enviados pelo usuário.
   - `folder__isnull=True`
     - Arquivos que não estão em nenhuma pasta.
   - `is_deleted=False`
     - Ignora arquivos deletados (soft delete).

```python
breadcrumbs = []  # Raiz não tem caminho
```

 - **Introdução:**
   - Define explicitamente que a raiz não possui caminho hierárquico.
 - **Codificação:**
   - Lista vazia.

```python
# Contexto do template
context = {
    "current_folder": current_folder,
    "folders": folders,
    "files": files,
    "breadcrumbs": breadcrumbs,
}
```

 - **Introdução:**
   - Esse bloco prepara os dados que serão enviados para o template HTML.
 - **Codificação:**
   - `"current_folder": current_folder`
     - Pasta atual (ou None).
   - `"folders": folders`
     - Lista de pastas (folders) a serem exibidas.
   - `"files": files`
     - Lista de arquivos (files) a serem exibidos.
   - `"breadcrumbs": breadcrumbs`
     - Caminho hierárquico completo.
     - Caminho de navegação.

```python
return render(request, "pages/workspace_home.html", context)
```

 - **Introdução:**
   - Esse bloco renderiza a página HTML do workspace.
 - **Codificação:**
   - `context`
     - Dados enviados para o template.
     - **Resultado:** HTML final exibido ao usuário.










---

<div id="workspace-view-create-folder"></div>

## `create_folder()`

> Essa view é responsável por criar uma nova pasta no workspace.

Ela lida com:

 - envio de formulário (POST);
 - validação de dados;
 - prevenção de nomes duplicados;
 - associação da pasta ao usuário e à pasta pai;
 - feedback visual (mensagens de sucesso ou erro).
 - reconstrução do estado da navegação em caso de erro.

> **NOTE:**  
> Ela funciona como um **handler de ação**, não como uma página independente.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def create_folder(request):

    if request.method == "POST":

        form = FolderForm(request.POST)

        # Obtem a pasta pai (se aplicável)
        parent_id = request.POST.get("parent")
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(
                Folder, id=parent_id, owner=request.user
            )

        if form.is_valid():
            name = form.cleaned_data["name"]

            # Verifica duplicação (ignorando caixa alta/baixa)
            if Folder.objects.filter(
                owner=request.user,
                name__iexact=name,
                parent=parent_folder,
                is_deleted=False
            ).exists():
                form.add_error(
                    "name",
                    "Já existe uma pasta com esse nome nesse diretório.",
                )
            else:
                # Criar nova pasta
                new_folder = form.save(commit=False)
                new_folder.owner = request.user
                new_folder.parent = parent_folder
                new_folder.save()

                messages.success(
                    request, f"Pasta '{name}' criada com sucesso!"
                )
                return redirect(request.POST.get("next", "workspace_home"))

        if parent_folder:
            # Estamos dentro de uma pasta
            folders = Folder.objects.filter(
                parent=parent_folder, is_deleted=False
            )
            files = File.objects.filter(
                folder=parent_folder, is_deleted=False
            )
            breadcrumbs = build_breadcrumbs(parent_folder)
        else:
            # Estamos na raiz
            folders = Folder.objects.filter(
                owner=request.user, parent__isnull=True, is_deleted=False
            )
            files = File.objects.filter(
                uploader=request.user, folder__isnull=True, is_deleted=False
            )
            breadcrumbs = []

        context = {
            "form": form,
            "current_folder": parent_folder,
            "folders": folders,
            "files": files,
            "breadcrumbs": breadcrumbs,
            "show_modal": True,  # reabrir modal com erro
        }

        return render(request, "pages/workspace_home.html", context)

    # Se método não for POST, redireciona para a home
    return redirect("workspace_home")
```

Agora, vamos explicar algumas partes do código acima (só o necessário, sem repetir o que já foi explicado em outras partes do README):

```python
if request.method == "POST":
    ...

return redirect("workspace_home")
```

 - `if request.method == "POST":`
   - Esse bloco garante que a criação de pasta só aconteça quando o formulário for enviado.
   - Quando é utilizado:
     - Quando o usuário clica em “Criar pasta”;
     - Quando o navegador envia os dados via POST
 - `return redirect("workspace_home")`
   - **Quando não recebe POST:**
   - A view não processa dados;
   - Redireciona para a página principal;
   - Evita acesso direto via URL (GET);
   - Isso protege a lógica e segue boas práticas REST.

```python
form = FolderForm(request.POST)
```

 - **Introdução:**
   - Cria uma instância do formulário Django preenchida com os dados enviados pelo usuário.
     - `FolderForm` → classe do formulário.
     - `request.POST` → dados do formulário.

```python
parent_id = request.POST.get("parent")
parent_folder = None
if parent_id:
    parent_folder = get_object_or_404(
        Folder, id=parent_id, owner=request.user
    )
```

 - **Introdução:**
   - Esse bloco determina onde a nova pasta será criada:
     - dentro de outra pasta;
     - ou na raiz.
 - **Codificação:**
   - `parent_id = request.POST.get("parent")`
     - Obtém o ID da pasta pai enviado pelo formulário.
   - `parent_folder = None`
     - Inicializa como None (caso seja raiz).
   - `if parent_id:`
     - Verifica se o usuário escolheu uma pasta pai.
     - `parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)`
       - Busca a pasta pai:
         - garante que existe;
         - garante que pertence ao usuário.

```python
if form.is_valid():
    name = form.cleaned_data["name"]
```

 - **Introdução:**
   - Esse bloco executa todas as validações do formulário.
 - **Codificação:**
   - `if form.is_valid():`
     - Executa validações automáticas e customizadas.
     - `is_valid()`
       - **is_valid()** serve para validar os dados enviados pelo usuário.
       - É um método da classe `django.forms.Form`;
       - Também presente em `django.forms.ModelForm`;
       - **NOTE:** Como `FolderForm` herda de uma dessas classes, ela ganha automaticamente o método `is_valid()`.
   - `name = form.cleaned_data["name"]`
     - Obtém o nome da pasta validado.
     - `cleaned_data`
       - cleaned_data é um dicionário com os dados finais e seguros do formulário.
       - Ele contém:
         - Apenas campos válidos.
         - Valores:
           - sanitizados;
           - normalizados;
           - convertidos para o tipo correto.

```python
if Folder.objects.filter(
    owner=request.user,
    name__iexact=name,
    parent=parent_folder,
    is_deleted=False
).exists():
```

 - **Introdução:**
   - Evita que o usuário crie duas pastas com o mesmo nome no mesmo diretório.
 - **Codificação:**
   - `owner=request.user` → somente pastas do usuário;
   - `name__iexact=name` → ignora maiúsculas/minúsculas;
   - `parent=parent_folder` → no mesmo nível;
   - `is_deleted=False` → ignora soft delete;
   - `.exists()` → retorna True ou False.

```python
form.add_error(
    "name",
    "Já existe uma pasta com esse nome nesse diretório.",
)
```

 - **Introdução:**
   - **Se existir duplicação.**
   - Associa erro ao campo;
   - Exibe no formulário.

```python
new_folder = form.save(commit=False)
new_folder.owner = request.user
new_folder.parent = parent_folder
new_folder.save()
```

 - **Introdução:**
   - **Se NÃO existir duplicação.**
   - Cria uma nova pasta.
 - **Codificação:**
   - `new_folder = form.save(commit=False)`
     - Cria o objeto sem salvar ainda.
   - `new_folder.owner = request.user`
     - Define o dono.
   - `new_folder.parent = parent_folder`
     - Define a pasta pai (ou None).
   - `new_folder.save()`
     - Salva no banco.

```python
if parent_folder:
    ...
else:
    ...
```

 - **Introdução:**
   - Esse bloco recria a tela exatamente como estava antes do erro, evitando que o usuário “perca” a navegação.
 - **Codificação:**
   - `Quando if parent_folder`
     - Usuário estava dentro de uma pasta.
   - `Quando else`
     - Usuário estava na raiz.

```python
context = {
    "form": form,
    "current_folder": parent_folder,
    "folders": folders,
    "files": files,
    "breadcrumbs": breadcrumbs,
    "show_modal": True,  # reabrir modal com erro
}
```

 - **Introdução:**
   - Esse dicionário contém todos os dados necessários para renderizar a página corretamente, incluindo erros.
   - `form` → com erros.
   - `show_modal=True` → reabre o modal.

```python
return render(request, "pages/workspace_home.html", context)
```

 - **O que é context?**
   - É o canal de comunicação entre a view e o template.
   - Ele permite usar no HTML:
     - `{{ folders }}`
     - `{{ form.errors }}`
     - `{{ breadcrumbs }}`
 - **Para que serve?**
   - exibir dados;
   - exibir erros;
   - controlar comportamento visual;
   - **NOTE:** Sem *context*, o template seria *“cego”*.










---

<div id="workspace-view-upload-file"></div>

## `upload_file()`

 - A view **upload_file()** é responsável por receber arquivos enviados pelo usuário no workspace, garantindo segurança, organização e boa experiência de uso.
 - Ela só permite upload para usuários autenticados e implementa um fluxo completo e robusto de upload.

Em alto nível, essa view:

 - 🔐 Exige login (@login_required)
 - 📥 Recebe arquivos via POST (request.FILES)
 - 📁 Associa o arquivo a uma pasta (ou à raiz)
 - 🔍 Valida tipo e tamanho do arquivo
 - 🔄 Evita sobrescrita renomeando automaticamente arquivos duplicados
 - 💾 Salva o arquivo no banco e no sistema de arquivos
 - 💬 Retorna feedback ao usuário via mensagens
 - 🔁 Redireciona o usuário de volta ao workspace correto

[views.py](workspace/views.py)
```python

@login_required(login_url="/")
def upload_file(request):
    """
    View que faz upload de arquivos com:
    - validação de extensão
    - validação de tamanho
    - renome automático em caso de duplicação
    """
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        next_url = request.POST.get("next", "workspace_home")
        folder_id = request.POST.get("folder")
        folder = None

        # pegar pasta atual se existir
        if folder_id:
            folder = get_object_or_404(
                Folder, id=folder_id, owner=request.user
            )

        # nenhum arquivo enviado
        if not uploaded_file:
            messages.error(request, "Nenhum arquivo foi enviado.")
            return redirect(next_url)

        # ------------------------------
        # 🔍 Validações via validators.py
        # ------------------------------
        try:
            validate_file(uploaded_file)
        except Exception as e:
            # pega somente a mensagem, não a lista
            messages.error(request, e.message)
            return redirect(next_url)

        # -------------------------------------
        # 🔄 Renome automático em caso de duplicação
        # -------------------------------------
        original_name = uploaded_file.name
        base, ext = os.path.splitext(original_name)
        new_name = original_name
        counter = 1

        while File.objects.filter(
            uploader=request.user,
            folder=folder,
            name__iexact=new_name,
            is_deleted=False
        ).exists():
            new_name = f"{base} ({counter}){ext}"
            counter += 1

        # ------------------------------
        # 💾 Criação do arquivo
        # ------------------------------
        File.objects.create(
            name=new_name,
            file=uploaded_file,
            folder=folder,
            uploader=request.user,
        )

        messages.success(request, f"Arquivo '{new_name}' enviado com sucesso!")
        return redirect(next_url)

    return redirect("workspace_home")
```










---

<div id="workspace-view-build-breadcrumbs"></div>

## `build_breadcrumbs()`

> A função **build_breadcrumbs()** é uma função utilitária usada para construir o caminho hierárquico de pastas (breadcrumbs) dentro do workspace.

[views.py](workspace/views.py)
```python
def build_breadcrumbs(folder):
    """
    Constrói a lista de breadcrumbs (caminho completo)
    desde a raiz até a pasta atual.
    """
    breadcrumbs = []
    while folder:
        breadcrumbs.insert(0, folder)
        folder = folder.parent
    return breadcrumbs
```










---

<div id="workspace-view-delete-folder"></div>

## `delete_folder()`

 - A view **delete_folder()** é responsável por *"excluir logicamente (soft delete)"* uma pasta do workspace do usuário.
 - Em vez de remover o registro do banco de dados, ela implementa um soft delete, marcando a pasta como deletada (is_deleted = True) e registrando a data da exclusão.

Essa abordagem permite:

 - 🗑️ uso de lixeira;
 - 🔒 recuperação futura;
 - 📊 histórico e auditoria;
 - 🚫 evitar perda definitiva de dados.

Além disso, a view:

 - garante que o usuário só possa excluir suas próprias pastas;
 - redireciona o usuário corretamente após a exclusão;
 - fornece feedback visual com mensagens.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    # pasta pai p/ retornar após exclusão
    parent = folder.parent

    folder.is_deleted = True
    folder.deleted_at = timezone.now()
    folder.save()

    messages.success(request, f"Pasta '{folder.name}' movida para a lixeira.")

    if parent:
        return redirect(f"/workspace?folder={parent.id}")

    return redirect("workspace_home")
```










---

<div id="workspace-view-delete-file"></div>

## `delete_file()`

 - A view **delete_file()** é responsável por excluir logicamente (soft delete) um arquivo do workspace do usuário.
 - Assim como na exclusão de pastas, o arquivo não é removido fisicamente do banco nem do disco, apenas é marcado como deletado.

Essa abordagem permite:

 - 🗑️ uso de lixeira;
 - 🔄 possível restauração futura;
 - 🛡️ evitar perda definitiva de dados;
 - 📜 manter histórico.

A view também:

 - garante que o usuário só possa excluir arquivos que ele mesmo enviou;
 - redireciona corretamente para a pasta atual;
 - fornece feedback visual ao usuário.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, uploader=request.user)

    folder = file.folder

    file.is_deleted = True
    file.deleted_at = timezone.now()
    file.save()

    messages.success(request, f"Arquivo '{file.name}' movido para a lixeira.")

    if folder:
        return redirect(f"/workspace?folder={folder.id}")

    return redirect("workspace_home")
```










---

<div id="workspace-view-rename-folder"></div>

## `rename_folder()`

> A view **rename_folder()** é responsável por *renomear* uma pasta existente no workspace do usuário, garantindo segurança, consistência e integridade dos dados.

Ela implementa regras importantes de negócio:

 - 🔐 Só usuários autenticados podem renomear pastas;
 - 👤 O usuário só pode renomear pastas que são dele;
 - 🗑️ Pastas já deletadas não podem ser renomeadas;
 - ✏️ O novo nome não pode ser vazio;
 - 🚫 Não pode haver nomes duplicados no mesmo diretório;
 - 🔄 Mantém o usuário no mesmo local após a ação (next).

> **NOTE:**  
> Essa *view* é uma *view* de ação (não renderiza template), usada normalmente por formulários ou modais de renomeação.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def rename_folder(request, folder_id):
    folder = get_object_or_404(
        Folder, id=folder_id, owner=request.user, is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    if not new_name:
        messages.error(request, "O nome da pasta não pode ser vazio.")
        return redirect(next_url)

    # impedir duplicatas no mesmo parent (case-insensitive), exceto a própria
    if Folder.objects.filter(
        owner=request.user,
        parent=folder.parent,
        name__iexact=new_name,
        is_deleted=False,
    ).exclude(id=folder.id).exists():
        messages.error(
            request, "Já existe uma pasta com esse nome nesse diretório."
        )
        return redirect(next_url)

    folder.name = new_name
    folder.save()
    messages.success(request, f"Pasta renomeada para '{new_name}'.")
    return redirect(next_url)
```










---

<div id="workspace-view-rename-file"></div>

## `rename_file()`

> A view **rename_file()** é responsável por *renomear* um arquivo existente no workspace do usuário, aplicando as mesmas regras de segurança e consistência usadas no renomeio de pastas.

Ela garante que:

 - 🔐 Apenas usuários autenticados possam renomear arquivos;
 - 👤 O usuário só possa renomear arquivos que ele enviou;
 - 🗑️ Arquivos deletados não possam ser alterados;
 - ✏️ O novo nome não seja vazio;
 - 🚫 Não existam nomes duplicados no mesmo diretório;
 - 🧭 O usuário permaneça no mesmo local após a ação.

> **NOTE:**  
> Essa *view* é uma view de ação (não renderiza template), normalmente acionada por um formulário ou modal.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def rename_file(request, file_id):
    file = get_object_or_404(
        File, id=file_id, uploader=request.user, is_deleted=False
    )

    if request.method != "POST":
        return redirect("workspace_home")

    new_name = request.POST.get("name", "").strip()
    next_url = request.POST.get("next", "workspace_home")

    if not new_name:
        messages.error(request, "O nome do arquivo não pode ser vazio.")
        return redirect(next_url)

    # impedir duplicatas no mesmo diretório (case-insensitive),
    # exceto o próprio
    if File.objects.filter(
        uploader=request.user,
        folder=file.folder,
        name__iexact=new_name,
        is_deleted=False,
    ).exclude(id=file.id).exists():
        messages.error(
            request, "Já existe um arquivo com esse nome neste diretório."
        )
        return redirect(next_url)

    file.name = new_name
    file.save()
    messages.success(request, f"Arquivo renomeado para '{new_name}'.")
    return redirect(next_url)
```










---

<div id="workspace-view-is-descendant"></div>

## `_is_descendant()`

> A função `_is_descendant()` é um helper interno (função auxiliar) usada para proteger a hierarquia de pastas do sistema.

O objetivo dela é evitar operações inválidas, como:

 - mover uma pasta para dentro dela mesma;
 - mover uma pasta para dentro de um de seus próprios filhos (ou netos).

Esse tipo de erro criaria um loop na árvore de pastas, quebrando toda a lógica de navegação, breadcrumbs e consultas recursivas.

> **NOTE:**  
> O `underscore (_)` no início do nome indica que ela é uma função interna, feita para uso apenas dentro do módulo.

[views.py](workspace/views.py)
```python
def _is_descendant(folder, potential_parent):
    """
    Helper para evitar mover uma pasta para ela mesma ou seus filhos.
    """
    current = potential_parent
    while current:
        if current == folder:
            return True
        current = current.parent
    return False
```










---

<div id="workspace-view-move-item"></div>

## `move_item()`

> A **view move_item()** é responsável por mover pastas ou arquivos dentro do workspace do usuário, alterando sua localização na hierarquia (mudando a pasta pai).

Ela foi pensada para ser usada em ações dinâmicas da interface (ex: drag-and-drop), por isso:

 - ✅ aceita apenas requisições POST
 - 🔁 não renderiza template
 - 📦 responde em JSON
 - 🔐 valida propriedade do item (segurança)
 - 🌳 protege a hierarquia de pastas contra loops
 - 📁 funciona tanto para pastas quanto para arquivos

> **NOTE:**  
> Essa view é um endpoint de API interna, não uma página.

[views.py](workspace/views.py)
```python
@login_required(login_url="/")
def move_item(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido."}, status=405)

    item_type = request.POST.get("item_type")
    item_id = request.POST.get("item_id")
    target_folder_id = request.POST.get("target_folder") or None

    if not item_type or not item_id:
        return JsonResponse(
            {"error": "Dados insuficientes para mover o item."}, status=400
        )

    target_folder = None
    if target_folder_id:
        target_folder = get_object_or_404(
            Folder,
            id=target_folder_id,
            owner=request.user,
            is_deleted=False,
        )

    if item_type == "folder":
        folder = get_object_or_404(
            Folder,
            id=item_id,
            owner=request.user,
            is_deleted=False,
        )

        if target_folder and _is_descendant(folder, target_folder):
            error_message = (
                "Não é possível mover a pasta para dentro dela mesma."
            )
            return JsonResponse(
                {"error": error_message},
                status=400,
            )

        folder.parent = target_folder
        folder.save()
        return JsonResponse({"success": True})

    elif item_type == "file":
        file = get_object_or_404(
            File,
            id=item_id,
            uploader=request.user,
            is_deleted=False,
        )
        file.folder = target_folder
        file.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Tipo de item inválido."}, status=400)
```





































































































<!--- ( Configurações ) --->

---

<div id="settings-google-auth"></div>

## `[Google Auth] Configuração do Google OAuth (login social)`

Aqui você vai aprender como configurar o **Google OAuth (login social)** no Django:

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

### Registrando o provedor do Google Auth no Django Admin

 - 1️⃣ Acesse: http://localhost:/admin/
 - 2️⃣ Vá em: Social Accounts → Social Applications → Add Social Application
 - 3️⃣ Crie o do Google:
   - Provider: Google
   - Name: Google Login
   - Client ID: (cole o do Google)
   - Secret Key: (cole o secret)
   - Por fim, vá em `Sites`:
     - *"Available sites"*
     - *"Choose sites by selecting them and then select the "Choose" arrow button"*
       - Adicione (Se não tiver): localhost:8000
       - Selecione localhost:8000 e aperta na seta `->`










---

<div id="settings-github-auth"></div>

## `[GitHub Auth] Configuração do GitHub OAuth (login social)`

<div id="settings-google-auth"></div>

Aqui você vai aprender como configurar o **GitHub OAuth (login social)** no Django:

 - Vá em https://github.com/settings/developers
 - Clique em OAuth Apps → New OAuth App
 - Preencha:
   - *Application name:* Easy RAG
   - *Homepage URL:* http://localhost:8000
   - *Authorization callback URL:* http://localhost:8000/accounts/github/login/callback/
 - Clique em `Register Application`
 - Copie o `Client ID`
 - Clique em `Generate new client secret` e copie o `Client Secret`

### Registrando o provedor do GitHub Auth no Django Admin

 - 1️⃣ Acesse: http://localhost:/admin/
 - 2️⃣ Vá em: Social Accounts → Social Applications → Add Social Application
 - 3️⃣ Crie o do GitHub:
   - Provider: GitHub
   - Name: GitHub Login
   - Client ID: (cole o do GitHub)
   - Secret Key: (cole o secret)
   - Por fim, vá em `Sites`:
     - *"Available sites"*
     - *"Choose sites by selecting them and then select the "Choose" arrow button"*
       - Adicione (Se não tiver): localhost:8000
       - Selecione localhost:8000 e aperta na seta `->`

---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
