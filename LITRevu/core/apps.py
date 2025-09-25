"""
Configuration de l'application Core.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration de l'application Django 'core'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"
