"""
Modèles pour la gestion des abonnements et des blocages entre utilisateurs.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class UserFollows(models.Model):
    """
    Représente un abonnement d’un utilisateur vers un autre.

    Attributs :
        - user : l’utilisateur qui suit.
        - followed_user : l’utilisateur suivi.
        - created_at : date de création de l’abonnement.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Utilisateur",
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
        verbose_name="Utilisateur suivi",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        unique_together = ("user", "followed_user")  # Un utilisateur ne peut pas suivre deux fois le même

    def __str__(self):
        """Retourne une représentation lisible de l’abonnement."""
        return f"{self.user.username} suit {self.followed_user.username}"


class UserBlock(models.Model):
    """
    Représente un blocage d’un utilisateur vers un autre.

    Attributs :
        - user : l’utilisateur qui bloque.
        - blocked_user : l’utilisateur bloqué.
        - created_at : date de création du blocage.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name="Utilisateur",
    )
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        verbose_name="Utilisateur bloqué",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Blocage"
        verbose_name_plural = "Blocages"
        unique_together = ("user", "blocked_user")

    def __str__(self):
        """Retourne une représentation lisible du blocage."""
        return f"{self.user.username} bloque {self.blocked_user.username}"
