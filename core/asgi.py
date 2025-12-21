"""
Configuração ASGI para o projeto core.

Expõe o callable ASGI como uma variável de nível de módulo chamada
``application``.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

ASGI (Asynchronous Server Gateway Interface) é usado para aplicações
assíncronas e suporta WebSockets, além de requisições HTTP tradicionais.
"""
import os

from django.core.asgi import get_asgi_application

# Define o módulo de configurações do Django
# Necessário antes de importar qualquer código Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Aplicação ASGI exposta para o servidor
# Esta variável é usada pelo servidor ASGI (ex: Uvicorn, Daphne)
application = get_asgi_application()
