"""
Configuration de l’application Tickets.
Permet de personnaliser le comportement de l’app dans l’admin Django.
"""

from django.apps import AppConfig


class TicketsConfig(AppConfig):
    """
    Configuration de l’app `tickets`.
    - Définit l’auto_field par défaut.
    - Spécifie le nom de l’application et son label lisible.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "tickets"
    verbose_name = "Tickets"
