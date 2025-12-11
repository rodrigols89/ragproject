# RAG Project

 - [**Introdução e Objetivos do Projeto**](#intro-to-the-project)
 - **Estrutura do Projeto:**
   - [`core/`](#core-project)
     - [`__init__.py`](#core-init-py)
     - [`asgi.py`](#core-asgi-py)
     - [`settings.py`](#core-settings-py)
     - [`urls.py`](#core-urls-py)
     - [`wsgi.py`](#core-wsgi-py)
 - **Configurações:**
   - [`[Google Auth] Configuração do Google OAuth (login social)`](#settings-google-auth)
   - [`[GitHub Auth] Configuração do GitHub OAuth (login social)`](#settings-github-auth)
<!---
[WHITESPACE RULES]
- Same topic = "10" Whitespace character.
- Different topic = "50" Whitespace character.
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


















































<!--- (  Estrutura do Projeto ) --->

---

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
