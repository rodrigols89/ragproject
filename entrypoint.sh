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
