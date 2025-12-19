import os

from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Configura Google e GitHub OAuth e cria superusuário "
        "automaticamente"
    )

    def handle(self, *args, **kwargs):
        site = self._setup_site()
        self._setup_providers(site)
        self._setup_superuser()

    def _setup_site(self):
        """Configura o Site do Django."""
        site_domain = (
            getattr(settings, "SITE_DOMAIN", None)
            or os.getenv("SITE_DOMAIN", "localhost:8000")
        )

        site_name = (
            getattr(settings, "SITE_NAME", None)
            or os.getenv("SITE_NAME", "localhost")
        )

        # Atualizar ou criar o Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                "domain": site_domain,
                "name": site_name,
            },
        )

        # Atualizar domínio se mudou
        if (
            site.domain != site_domain
            or site.name != site_name
        ):
            site.domain = site_domain
            site.name = site_name
            site.save()
            self.stdout.write(
                self.style.SUCCESS(f"Site atualizado: {site_domain}")
            )
        elif created:
            self.stdout.write(
                self.style.SUCCESS(f"Site criado: {site_domain}")
            )

        return site

    def _setup_providers(self, site):
        """Configura os provedores OAuth (Google e GitHub)."""
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

        for provider in providers:
            self._setup_provider(provider, site)

    def _setup_provider(self, provider, site):
        """Configura um único provedor OAuth."""
        if not provider["client_id"] or not provider["secret"]:
            provider_name = provider['provider']
            client_id_status = '✓' if provider['client_id'] else '✗'
            secret_status = '✓' if provider['secret'] else '✗'
            msg = (
                f"⚠️  Variáveis não definidas para {provider_name}. "
                f"Client ID: {client_id_status}, "
                f"Secret: {secret_status}"
            )
            self.stdout.write(self.style.WARNING(msg))
            return

        app, created = SocialApp.objects.get_or_create(
            provider=provider["provider"],
            defaults={
                "name": provider["name"],
                "client_id": provider["client_id"],
                "secret": provider["secret"],
            },
        )

        updated = self._update_provider_credentials(app, provider)

        # Garantir que o site está associado ao SocialApp
        if site not in app.sites.all():
            app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Site associado ao {provider['name']}"
                )
            )

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
        """Atualiza as credenciais do provedor se necessário."""
        updated = False
        if app.client_id != provider["client_id"]:
            app.client_id = provider["client_id"]
            updated = True
        if app.secret != provider["secret"]:
            app.secret = provider["secret"]
            updated = True
        if updated:
            app.save()
            provider_name = provider['name']
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {provider_name} atualizado com novas credenciais"
                )
            )
        return updated

    def _setup_superuser(self):
        """Cria ou atualiza o superusuário."""
        admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if admin_username and admin_password:
            user_exists = User.objects.filter(
                username=admin_username
            ).exists()
            if not user_exists:
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
                self._update_superuser(
                    admin_username, admin_email, admin_password
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  Variáveis DJANGO_SUPERUSER_USERNAME e "
                    "DJANGO_SUPERUSER_PASSWORD não definidas. "
                    "Execute 'python manage.py createsuperuser' "
                    "manualmente."
                )
            )

    def _update_superuser(self, username, email, password):
        """Atualiza a senha e email do superusuário existente."""
        user = User.objects.get(username=username)
        user.set_password(password)
        if email:
            user.email = email
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Senha do superusuário '{username}' "
                "atualizada"
            )
        )
