"""
Comando de gerenciamento para configuração inicial do projeto.

Este comando automatiza a configuração inicial do projeto Django,
incluindo:
- Configuração do Site do Django
- Configuração de provedores OAuth (Google e GitHub)
- Criação de superusuário inicial

Uso:
    python manage.py init_setup

Requisitos:
    - Variáveis de ambiente configuradas para OAuth e superusuário
"""
import os

from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

User = get_user_model()


# ============================================================================
# COMANDO DE CONFIGURAÇÃO INICIAL
# ============================================================================

class Command(BaseCommand):
    """
    Comando de gerenciamento para configuração inicial.

    Configura automaticamente o site, provedores OAuth e cria
    o superusuário inicial baseado em variáveis de ambiente.
    """

    help = (
        "Configura Google e GitHub OAuth e cria superusuário "
        "automaticamente"
    )

    def handle(self, *args, **kwargs):
        """
        Método principal executado quando o comando é chamado.

        Orquestra a configuração de todas as partes necessárias:
        site, provedores OAuth e superusuário.
        """
        site = self._setup_site()
        self._setup_providers(site)
        self._setup_superuser()

    # ========================================================================
    # CONFIGURAÇÃO DO SITE
    # ========================================================================

    def _setup_site(self):
        """
        Configura o Site do Django.

        O Site é necessário para o funcionamento do django-allauth.
        Cria ou atualiza o site com base nas configurações do projeto.

        Returns:
            Site: Objeto Site configurado
        """
        # Obtém domínio do site das configurações ou variáveis de ambiente
        site_domain = (
            getattr(settings, "SITE_DOMAIN", None)
            or os.getenv("SITE_DOMAIN", "localhost:8000")
        )

        # Obtém nome do site das configurações ou variáveis de ambiente
        site_name = (
            getattr(settings, "SITE_NAME", None)
            or os.getenv("SITE_NAME", "localhost")
        )

        # Cria ou obtém o site (sempre com ID 1)
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                "domain": site_domain,
                "name": site_name,
            },
        )

        # Atualiza domínio e nome se mudaram
        if (
            site.domain != site_domain
            or site.name != site_name
        ):
            site.domain = site_domain
            site.name = site_name
            site.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Site atualizado: {site_domain}"
                )
            )
        elif created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Site criado: {site_domain}"
                )
            )

        return site

    # ========================================================================
    # CONFIGURAÇÃO DE PROVEDORES OAUTH
    # ========================================================================

    def _setup_providers(self, site):
        """
        Configura os provedores OAuth (Google e GitHub).

        Itera sobre a lista de provedores e configura cada um,
        associando-os ao site fornecido.

        Args:
            site: Objeto Site ao qual os provedores serão associados
        """
        # Lista de provedores OAuth a serem configurados
        providers = [
            {
                "provider": "google",
                "name": "Google",
                "client_id": (
                    getattr(settings, "GOOGLE_CLIENT_ID", None)
                    or os.getenv("GOOGLE_CLIENT_ID")
                ),
                "secret": (
                    getattr(settings, "GOOGLE_CLIENT_SECRET", None)
                    or os.getenv("GOOGLE_CLIENT_SECRET")
                ),
            },
            {
                "provider": "github",
                "name": "GitHub",
                "client_id": (
                    getattr(settings, "GITHUB_CLIENT_ID", None)
                    or os.getenv("GITHUB_CLIENT_ID")
                ),
                "secret": (
                    getattr(settings, "GITHUB_CLIENT_SECRET", None)
                    or os.getenv("GITHUB_CLIENT_SECRET")
                ),
            },
        ]

        # Configura cada provedor
        for provider in providers:
            self._setup_provider(provider, site)

    def _setup_provider(self, provider, site):
        """
        Configura um único provedor OAuth.

        Cria ou atualiza o SocialApp para o provedor especificado,
        associando-o ao site fornecido.

        Args:
            provider: Dicionário com informações do provedor
            site: Objeto Site ao qual o provedor será associado
        """
        # Verifica se as credenciais estão definidas
        if not provider["client_id"] or not provider["secret"]:
            provider_name = provider['provider']
            client_id_status = (
                '✓' if provider['client_id'] else '✗'
            )
            secret_status = '✓' if provider['secret'] else '✗'
            msg = (
                f"⚠️  Variáveis não definidas para {provider_name}. "
                f"Client ID: {client_id_status}, "
                f"Secret: {secret_status}"
            )
            self.stdout.write(self.style.WARNING(msg))
            return

        # Cria ou obtém o SocialApp para o provedor
        app, created = SocialApp.objects.get_or_create(
            provider=provider["provider"],
            defaults={
                "name": provider["name"],
                "client_id": provider["client_id"],
                "secret": provider["secret"],
            },
        )

        # Atualiza credenciais se necessário
        updated = self._update_provider_credentials(app, provider)

        # Garante que o site está associado ao SocialApp
        if site not in app.sites.all():
            app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Site associado ao {provider['name']}"
                )
            )

        # Mensagens de feedback
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {provider['name']} criado e configurado"
                )
            )
        elif not updated:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {provider['name']} já estava configurado"
                )
            )

    def _update_provider_credentials(self, app, provider):
        """
        Atualiza as credenciais do provedor se necessário.

        Compara as credenciais atuais com as novas e atualiza
        se houver diferença.

        Args:
            app: Objeto SocialApp a ser atualizado
            provider: Dicionário com novas credenciais

        Returns:
            bool: True se houve atualização, False caso contrário
        """
        updated = False

        # Atualiza client_id se mudou
        if app.client_id != provider["client_id"]:
            app.client_id = provider["client_id"]
            updated = True

        # Atualiza secret se mudou
        if app.secret != provider["secret"]:
            app.secret = provider["secret"]
            updated = True

        # Salva se houve atualização
        if updated:
            app.save()
            provider_name = provider['name']
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {provider_name} atualizado com novas "
                    "credenciais"
                )
            )

        return updated

    # ========================================================================
    # CONFIGURAÇÃO DO SUPERUSUÁRIO
    # ========================================================================

    def _setup_superuser(self):
        """
        Cria ou atualiza o superusuário inicial.

        Lê as credenciais das variáveis de ambiente e cria ou
        atualiza o superusuário conforme necessário.
        """
        # Obtém credenciais das variáveis de ambiente
        admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        # Cria ou atualiza o superusuário se as credenciais existirem
        if admin_username and admin_password:
            user_exists = User.objects.filter(
                username=admin_username
            ).exists()

            if not user_exists:
                # Cria novo superusuário
                User.objects.create_superuser(
                    username=admin_username,
                    email=admin_email or "",
                    password=admin_password
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Superusuário '{admin_username}' "
                        "criado com sucesso"
                    )
                )
            else:
                # Atualiza superusuário existente
                self._update_superuser(
                    admin_username,
                    admin_email,
                    admin_password
                )
        else:
            # Avisa se as variáveis não estiverem definidas
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  Variáveis DJANGO_SUPERUSER_USERNAME e "
                    "DJANGO_SUPERUSER_PASSWORD não definidas. "
                    "Execute 'python manage.py createsuperuser' "
                    "manualmente."
                )
            )

    def _update_superuser(self, username, email, password):
        """
        Atualiza a senha e email do superusuário existente.

        Útil para atualizar credenciais sem precisar deletar e
        recriar o usuário.

        Args:
            username: Nome de usuário do superusuário
            email: Novo email (opcional)
            password: Nova senha
        """
        user = User.objects.get(username=username)
        user.set_password(password)

        # Atualiza email se fornecido
        if email:
            user.email = email

        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Senha do superusuário '{username}' "
                "atualizada"
            )
        )
