"""
Configuration de l'application Authentication.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Classe de configuration pour l'application d'authentification.

    - Définit l'identifiant de l'application.
    - Ajoute un nom lisible dans l'interface d'administration Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
    verbose_name = "Authentification"
