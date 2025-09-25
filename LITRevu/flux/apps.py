"""
Configuration de l'application Flux.
"""

from django.apps import AppConfig


class FluxConfig(AppConfig):
    """Configuration de l'application Django 'flux'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "flux"
    verbose_name = "Flux"
