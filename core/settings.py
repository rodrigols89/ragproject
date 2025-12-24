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

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-ntyi#32b20l03ioo=3tr=1j8snafe(7*l=#)u&6+rdyrk)6v7f'
)

DEBUG = (
    os.getenv('DJANGO_DEBUG', 'True').lower()
    in ('true', '1', 'yes')
)

allowed_hosts_env = os.getenv('DJANGO_ALLOWED_HOSTS', '')
if allowed_hosts_env == '*':
    ALLOWED_HOSTS = ['*']
elif allowed_hosts_env:
    ALLOWED_HOSTS = [
        host.strip()
        for host in allowed_hosts_env.split(',')
        if host.strip()
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "users",
    "workspace",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'

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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost:8000")
SITE_NAME = os.getenv("SITE_NAME", "localhost")

LOGIN_REDIRECT_URL = "/home/"

LOGOUT_REDIRECT_URL = "/"

SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_LOGIN_METHODS = {"username"}

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "username*",
    "password1*",
    "password2*",
]

ACCOUNT_EMAIL_VERIFICATION = "optional"

ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = (
    "users.adapter.NoMessageSocialAccountAdapter"
)


WSGI_APPLICATION = 'core.wsgi.application'

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


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


USE_X_FORWARDED_HOST = True

USE_X_FORWARDED_PORT = True

SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)


csrf_origins = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost,http://127.0.0.1'
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in csrf_origins.split(',')
    if origin.strip()
]


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
