"""
Adaptadores customizados para django-allauth.

Este módulo contém adaptadores que modificam o comportamento padrão
do django-allauth, especificamente para suprimir mensagens automáticas
que o allauth adicionaria ao sistema de mensagens do Django.
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter
)


class NoMessageAccountAdapter(DefaultAccountAdapter):
    """
    Adapter para suprimir mensagens automáticas do allauth.

    Sobrescreve o método add_message para evitar que o allauth adicione
    mensagens automáticas ao sistema de mensagens do Django. Isso é
    útil quando você quer controlar manualmente as mensagens exibidas
    ao usuário.

    Herda de DefaultAccountAdapter mas não chama super(), efetivamente
    desabilitando a funcionalidade de adicionar mensagens.
    """

    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None
    ):
        """
        Não adiciona mensagem ao sistema de mensagens.

        Sobrescreve o método padrão para evitar que mensagens automáticas
        do allauth sejam exibidas. Permite controle manual das mensagens
        através das views customizadas.

        Args:
            request: Objeto HttpRequest do Django
            level: Nível da mensagem (INFO, SUCCESS, ERROR, etc)
            message_template: Template da mensagem
            message_context: Contexto adicional para a mensagem

        Returns:
            None - Não adiciona nenhuma mensagem
        """
        return


class NoMessageSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adapter para suprimir mensagens de login social.

    Similar ao NoMessageAccountAdapter, mas específico para contas
    de login social (Google, GitHub, etc). Previne que mensagens
    automáticas sejam adicionadas durante o processo de autenticação
    social.

    Herda de DefaultSocialAccountAdapter mas não chama super(),
    efetivamente desabilitando a funcionalidade de adicionar mensagens.
    """

    def add_message(
        self,
        request,
        level,
        message_template,
        message_context=None
    ):
        """
        Não adiciona mensagem ao sistema de mensagens.

        Sobrescreve o método padrão para evitar que mensagens automáticas
        do allauth sejam exibidas durante login social. Permite controle
        manual das mensagens através das views customizadas.

        Args:
            request: Objeto HttpRequest do Django
            level: Nível da mensagem (INFO, SUCCESS, ERROR, etc)
            message_template: Template da mensagem
            message_context: Contexto adicional para a mensagem

        Returns:
            None - Não adiciona nenhuma mensagem
        """
        return
