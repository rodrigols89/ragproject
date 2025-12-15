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
       - [`pages/`](#users-pages-folder)
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

<div id="users-pages-folder"></div>

## `pages/`

> O diretório `users/templates/pages/` é onde ficam os templates das **páginas genéricas** do app users.










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
