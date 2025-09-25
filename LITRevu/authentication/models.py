"""
Modèles pour l'application d'authentification.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser.

    Ajoute un champ optionnel de photo de profil
    en plus des champs standards fournis par Django.
    """

    profile_photo = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text="Photo de profil de l'utilisateur (optionnelle).",
    )

    def __str__(self) -> str:
        """Retourne le nom d'utilisateur comme représentation texte."""
        return self.username
