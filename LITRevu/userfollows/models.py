from django.conf import settings
from django.db import models


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

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        unique_together = ("user", "followed_user")  # un utilisateur ne peut pas suivre deux fois le même

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
