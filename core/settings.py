import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-ntyi#32b20l03ioo=3tr=1j8snafe(7*l=#)u&6+rdyrk)6v7f'
)

DEBUG = (
    os.getenv('DEBUG', 'True').lower()
    in ('true', '1', 'yes')
)

ALLOWED_HOSTS = (
    os.getenv('ALLOWED_HOSTS', '').split(',')
    if os.getenv('ALLOWED_HOSTS')
    else ['localhost', '127.0.0.1']
)

# Application definition
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
    # 👈 habilita login com Google
    "allauth.socialaccount.providers.google",
    # 👈 habilita login com GitHub
    "allauth.socialaccount.providers.github",

    # Seus apps
    "users",
    "workspace",
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # ✅ Novo middleware exigido pelo Django Allauth
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    (
        'django.middleware.clickjacking.'
        'XFrameOptionsMiddleware'
    ),
]

ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': (
            'django.template.backends.django.DjangoTemplates'
        ),
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # <- Necessário para allauth
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                (
                    'django.contrib.messages.context_processors.'
                    'messages'
                ),
            ],
        },
    },
]

# AUTHENTICATION_BACKENDS
# combine o backend padrão com o do allauth
AUTHENTICATION_BACKENDS = [
    # Seu login normal
    "django.contrib.auth.backends.ModelBackend",
    # Login social
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = 'core.wsgi.application'

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

# Configurações de "Internacionalização"
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de Arquivos Estáticos (STATIC)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configurações de Arquivos de Mídia (MEDIA)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações de autenticação do Django + Allauth
SITE_ID = 1
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost:8000")
SITE_NAME = os.getenv("SITE_NAME", "localhost")
# ou o nome da rota que preferir
LOGIN_REDIRECT_URL = "/home/"
# para onde o usuário vai depois do logout
LOGOUT_REDIRECT_URL = "/"
# Login imediato ao clicar no link do provedor
SOCIALACCOUNT_LOGIN_ON_GET = True

# Permitir login apenas com username
# (pode ser {'username', 'email'} se quiser os dois)
ACCOUNT_LOGIN_METHODS = {"username"}

# Campos obrigatórios no cadastro
# (asterisco * indica que o campo é requerido)
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "username*",
    "password1*",
    "password2*",
]
# "mandatory" em produção
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = (
    "users.adapter.NoMessageSocialAccountAdapter"
)


# Configurações para funcionar atrás de proxy reverso (nginx)
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)

# CSRF Trusted Origins - necessário quando usando proxy reverso
csrf_origins = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost,http://127.0.0.1'
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_origins.split(',')
    if origin.strip()
]

# Configurações de cookies de sessão e CSRF
SESSION_COOKIE_SECURE = (
    os.getenv('SESSION_COOKIE_SECURE', 'False').lower()
    in ('true', '1', 'yes')
)
CSRF_COOKIE_SECURE = (
    os.getenv('CSRF_COOKIE_SECURE', 'False').lower()
    in ('true', '1', 'yes')
)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
