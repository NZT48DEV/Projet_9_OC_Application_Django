from django.conf import settings
from django.db import models
from django.utils import timezone


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",   # l’utilisateur qui suit
        verbose_name="Utilisateur"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",  # l’utilisateur suivi
        verbose_name="Utilisateur suivi"
    )
    created_at = models.DateTimeField(default=timezone.now)  # ✅ date d'abonnement

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        unique_together = ("user", "followed_user")  # un utilisateur ne peut pas suivre deux fois le même

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"


class UserBlock(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name="Utilisateur"
    )
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        verbose_name="Utilisateur bloqué"
    )
    created_at = models.DateTimeField(default=timezone.now)  # ✅ date de blocage

    class Meta:
        verbose_name = "Blocage"
        verbose_name_plural = "Blocages"
        unique_together = ("user", "blocked_user")

    def __str__(self):
        return f"{self.user.username} bloque {self.blocked_user.username}"
