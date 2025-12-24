"""
Configuração WSGI para o projeto core.

Expõe o callable WSGI como uma variável de nível de módulo chamada
``application``.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/

WSGI (Web Server Gateway Interface) é a interface padrão entre
servidores web e aplicações Python. Usado principalmente para deploy
em produção com servidores como Gunicorn, uWSGI, etc.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
