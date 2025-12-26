"""
Comando de gerenciamento Django para configurar provedores sociais
automaticamente a partir das variáveis de ambiente.
"""
import os

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Configura provedores sociais (Google e GitHub) a partir de '
        'variáveis de ambiente'
    )

    def handle(self, *args, **options):
        site_id = int(os.getenv("DJANGO_SITE_ID", "1"))
        site_domain = os.getenv(
            "DJANGO_SITE_DOMAIN", "localhost:8000"
        )
        site_name = os.getenv("DJANGO_SITE_NAME", "localhost")

        try:
            site = Site.objects.get(id=site_id)
            # Atualiza o site se ainda estiver com valores padrão
            if site.domain != site_domain or site.name != site_name:
                site.domain = site_domain
                site.name = site_name
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} atualizado: '
                        f'domain="{site_domain}", name="{site_name}"'
                    )
                )
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Site com ID {site_id} não encontrado. Criando...'
                )
            )
            site = Site.objects.create(
                id=site_id,
                domain=site_domain,
                name=site_name
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Site {site_id} criado: '
                    f'domain="{site_domain}", name="{site_name}"'
                )
            )

        # Configurar Google
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if google_client_id and google_client_secret:
            social_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': google_client_id,
                    'secret': google_client_secret,
                }
            )

            if not created:
                # Atualiza se já existir
                social_app.client_id = google_client_id
                social_app.secret = google_client_secret
                social_app.save()
                self.stdout.write(
                    self.style.WARNING('SocialApp Google atualizado.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'SocialApp Google criado com sucesso.'
                    )
                )

            # Garante que o site está associado
            if site not in social_app.sites.all():
                social_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} associado ao Google.'
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis GOOGLE_CLIENT_ID ou '
                    'GOOGLE_CLIENT_SECRET não encontradas. '
                    'Pulando configuração do Google.'
                )
            )

        # Configurar GitHub
        github_client_id = os.getenv("GITHUB_CLIENT_ID")
        github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

        if github_client_id and github_client_secret:
            social_app, created = SocialApp.objects.get_or_create(
                provider='github',
                defaults={
                    'name': 'GitHub',
                    'client_id': github_client_id,
                    'secret': github_client_secret,
                }
            )

            if not created:
                # Atualiza se já existir
                social_app.client_id = github_client_id
                social_app.secret = github_client_secret
                social_app.save()
                self.stdout.write(
                    self.style.WARNING('SocialApp GitHub atualizado.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'SocialApp GitHub criado com sucesso.'
                    )
                )

            # Garante que o site está associado
            if site not in social_app.sites.all():
                social_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Site {site_id} associado ao GitHub.'
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Variáveis GITHUB_CLIENT_ID ou '
                    'GITHUB_CLIENT_SECRET não encontradas. '
                    'Pulando configuração do GitHub.'
                )
            )
