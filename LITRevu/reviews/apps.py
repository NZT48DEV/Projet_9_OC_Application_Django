"""
Configuration de l'application Reviews.
Gère l'enregistrement et les paramètres par défaut de l'app dans Django.
"""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Configuration de l'application `reviews`."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
    verbose_name = "Critiques"
