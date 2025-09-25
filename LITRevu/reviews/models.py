"""
Modèles pour la gestion des critiques (reviews).
Chaque critique est liée à un ticket, possède une note, un titre et un corps de texte.
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Review(models.Model):
    """
    Modèle représentant une critique associée à un ticket.
    - Chaque review appartient à un utilisateur.
    - Elle contient un titre (headline), une note (rating) et un texte (body).
    - Une review est horodatée lors de sa création.
    """

    ticket = models.ForeignKey(
        to="tickets.Ticket",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Ticket auquel la critique est associée"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Note de 0 à 5"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Utilisateur ayant rédigé la critique"
    )
    body = models.TextField(
        max_length=8192,
        blank=True,
        help_text="Contenu principal de la critique"
    )
    headline = models.CharField(
        max_length=128,
        help_text="Titre de la critique"
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création"
    )

    def __str__(self):
        """Représentation textuelle lisible de la critique."""
        return f"{self.headline} - {self.rating}/5 par {self.user.username}"
