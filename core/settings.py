"""
Configurações do projeto Django.

Este arquivo contém todas as configurações necessárias para o
funcionamento do projeto, incluindo:
- Configurações de segurança e ambiente
- Aplicações instaladas e middleware
- Configurações de banco de dados
- Configurações de autenticação (Django + Allauth)
- Configurações de arquivos estáticos e mídia
- Configurações para proxy reverso
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ============================================================================
# CONFIGURAÇÕES DE CAMINHOS E DIRETÓRIOS
# ============================================================================

# Diretório base do projeto (raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# CONFIGURAÇÕES DE SEGURANÇA E AMBIENTE
# ============================================================================

# Chave secreta para assinatura de sessões e tokens
# Em produção, sempre use uma chave segura via variável de ambiente
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-ntyi#32b20l03ioo=3tr=1j8snafe(7*l=#)u&6+rdyrk)6v7f'
)

# Modo de debug (True em desenvolvimento, False em produção)
# Controla exibição de erros detalhados e informações de debug
DEBUG = (
    os.getenv('DJANGO_DEBUG', 'True').lower()
    in ('true', '1', 'yes')
)

# Hosts permitidos para acessar a aplicação
# Em produção, liste os domínios reais
# Use '*' para permitir qualquer host (apenas desenvolvimento)
allowed_hosts_env = os.getenv('DJANGO_ALLOWED_HOSTS', '')
if allowed_hosts_env == '*':
    # Permite qualquer host (apenas desenvolvimento)
    ALLOWED_HOSTS = ['*']
elif allowed_hosts_env:
    # Lista de hosts separados por vírgula
    ALLOWED_HOSTS = [
        host.strip()
        for host in allowed_hosts_env.split(',')
        if host.strip()
    ]
else:
    # Padrão: apenas localhost
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ============================================================================
# CONFIGURAÇÕES DE APLICAÇÕES INSTALADAS
# ============================================================================

INSTALLED_APPS = [
    # Aplicações padrão do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicação de sites (obrigatória para django-allauth)
    "django.contrib.sites",

    # Aplicações principais do django-allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Provedores de login social
    "allauth.socialaccount.providers.google",  # Login com Google
    "allauth.socialaccount.providers.github",  # Login com GitHub

    # Aplicações customizadas do projeto
    "users",
    "workspace",
]

# ============================================================================
# CONFIGURAÇÕES DE MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    # Middleware de segurança
    'django.middleware.security.SecurityMiddleware',

    # Middleware de sessão (gerencia sessões de usuário)
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Middleware comum (normaliza URLs, etc)
    'django.middleware.common.CommonMiddleware',

    # Middleware CSRF (proteção contra ataques CSRF)
    'django.middleware.csrf.CsrfViewMiddleware',

    # Middleware de autenticação (adiciona objeto user ao request)
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Middleware do django-allauth (gerencia contas e autenticação)
    'allauth.account.middleware.AccountMiddleware',

    # Middleware de mensagens (mensagens flash)
    'django.contrib.messages.middleware.MessageMiddleware',

    # Middleware de proteção contra clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================================
# CONFIGURAÇÕES DE URLS E TEMPLATES
# ============================================================================

# Módulo principal de URLs do projeto
ROOT_URLCONF = 'core.urls'

# Configurações de templates (HTML)
TEMPLATES = [
    {
        'BACKEND': (
            'django.template.backends.django.DjangoTemplates'
        ),
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Context processor de debug
                'django.template.context_processors.debug',

                # Context processor de request (necessário para allauth)
                'django.template.context_processors.request',

                # Context processor de autenticação (adiciona user)
                'django.contrib.auth.context_processors.auth',

                # Context processor de mídia
                'django.template.context_processors.media',

                # Context processor de arquivos estáticos
                'django.template.context_processors.static',

                # Context processor de timezone
                'django.template.context_processors.tz',

                # Context processor de mensagens
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO
# ============================================================================

# Backends de autenticação (ordem importa)
# Combina autenticação padrão do Django com django-allauth
AUTHENTICATION_BACKENDS = [
    # Backend padrão do Django (login com username/password)
    "django.contrib.auth.backends.ModelBackend",

    # Backend do django-allauth (login social e email)
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Configurações específicas do django-allauth
SITE_ID = 1  # ID do site no banco de dados
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost:8000")
SITE_NAME = os.getenv("SITE_NAME", "localhost")

# URL para redirecionar após login bem-sucedido
LOGIN_REDIRECT_URL = "/home/"

# URL para redirecionar após logout
LOGOUT_REDIRECT_URL = "/"

# Permite login imediato ao clicar no link do provedor social
# (sem página intermediária de confirmação)
SOCIALACCOUNT_LOGIN_ON_GET = True

# Métodos de login permitidos
# {'username'} = apenas username
# {'email'} = apenas email
# {'username', 'email'} = ambos
ACCOUNT_LOGIN_METHODS = {"username"}

# Campos obrigatórios no formulário de cadastro
# Campos marcados com * são obrigatórios
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "username*",
    "password1*",
    "password2*",
]

# Verificação de email
# "mandatory" = obrigatório verificar email
# "optional" = opcional verificar email
# "none" = não verificar email
ACCOUNT_EMAIL_VERIFICATION = "optional"

# Adaptadores customizados para desabilitar mensagens do allauth
ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = (
    "users.adapter.NoMessageSocialAccountAdapter"
)

# ============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS
# ============================================================================

WSGI_APPLICATION = 'core.wsgi.application'

# Configuração do banco de dados PostgreSQL
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

# ============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO DE SENHAS
# ============================================================================

# Validadores de senha aplicados durante criação/atualização
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# ============================================================================
# CONFIGURAÇÕES DE INTERNACIONALIZAÇÃO E TIMEZONE
# ============================================================================

# Idioma padrão da aplicação
LANGUAGE_CODE = "pt-br"

# Timezone padrão
TIME_ZONE = "America/Sao_Paulo"

# Habilita internacionalização (i18n)
USE_I18N = True

# Habilita timezone awareness
USE_TZ = True

# ============================================================================
# CONFIGURAÇÕES DE MODELOS
# ============================================================================

# Tipo de campo automático para chaves primárias
# Usa BigAutoField por padrão (suporta números maiores)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# CONFIGURAÇÕES DE ARQUIVOS ESTÁTICOS
# ============================================================================

# URL base para servir arquivos estáticos (CSS, JS, imagens)
STATIC_URL = '/static/'

# Diretórios adicionais onde o Django procura arquivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']

# Diretório onde arquivos estáticos são coletados para produção
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================================
# CONFIGURAÇÕES DE ARQUIVOS DE MÍDIA
# ============================================================================

# URL base para servir arquivos de mídia enviados pelos usuários
MEDIA_URL = '/media/'

# Diretório onde arquivos de mídia são armazenados
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# CONFIGURAÇÕES PARA PROXY REVERSO (NGINX, ETC)
# ============================================================================

# Usa o header X-Forwarded-Host para determinar o host
USE_X_FORWARDED_HOST = True

# Usa o header X-Forwarded-Port para determinar a porta
USE_X_FORWARDED_PORT = True

# Header usado para detectar requisições HTTPS através do proxy
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)

# ============================================================================
# CONFIGURAÇÕES DE CSRF (CROSS-SITE REQUEST FORGERY)
# ============================================================================

# Origens confiáveis para requisições CSRF
# Necessário quando usando proxy reverso ou CORS
csrf_origins = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost,http://127.0.0.1'
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_origins.split(',')
    if origin.strip()
]

# ============================================================================
# CONFIGURAÇÕES DE COOKIES DE SESSÃO E CSRF
# ============================================================================

# Cookie de sessão só é enviado via HTTPS (True em produção)
SESSION_COOKIE_SECURE = (
    os.getenv('SESSION_COOKIE_SECURE', 'False').lower()
    in ('true', '1', 'yes')
)

# Cookie CSRF só é enviado via HTTPS (True em produção)
CSRF_COOKIE_SECURE = (
    os.getenv('CSRF_COOKIE_SECURE', 'False').lower()
    in ('true', '1', 'yes')
)

# Política SameSite para cookies de sessão
# 'Lax' = envia cookies em requisições GET de outros sites
SESSION_COOKIE_SAMESITE = 'Lax'

# Política SameSite para cookies CSRF
CSRF_COOKIE_SAMESITE = 'Lax'

# ============================================================================
# CONFIGURAÇÕES DE PROVEDORES DE LOGIN SOCIAL
# ============================================================================

# Credenciais do Google OAuth2
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Credenciais do GitHub OAuth2
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
