#!/bin/bash
set -e

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
    # Executa o comando como appuser
    exec gosu appuser "$@"
else
    # Se já estiver rodando como appuser, apenas executa
    exec "$@"
fi
