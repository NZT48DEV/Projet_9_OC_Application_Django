"""
Modèles de l’application Tickets :
- Ticket : représente une demande de critique (livre ou article).
- Image  : gère une image associée à un ticket avec redimensionnement automatique.
"""

from django.conf import settings
from django.db import models
from PIL import Image as Img


class Ticket(models.Model):
    """
    Modèle représentant un ticket (demande de critique).
    - Peut concerner un livre ou un article.
    - Chaque ticket peut avoir une image associée (relation OneToOne avec Image).
    """
    TYPE_CHOICES = [
        ("", "Choisissez un type"),  # valeur vide affichée en premier
        ("BOOK", "Livre"),
        ("ARTICLE", "Article"),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        blank=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Affiche le titre et le type du ticket (ex. : Mon livre (Livre))."""
        return f"{self.title} ({self.get_type_display()})"


class Image(models.Model):
    """
    Modèle représentant une image associée à un ticket.
    - Chaque ticket peut avoir une seule image.
    - Redimensionne automatiquement l’image sauvegardée à 400x400px max.
    """
    image = models.ImageField()
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="image",
        null=True,
        blank=True,
    )
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def __str__(self) -> str:
        """Affiche le chemin de l’image."""
        return str(self.image)

    def resize_image(self) -> None:
        """
        Redimensionne l’image pour ne pas dépasser IMAGE_MAX_SIZE.
        Conserve les proportions (utilise PIL.Image.thumbnail).
        """
        image = Img.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs) -> None:
        """
        Sauvegarde l’image en base de données et redimensionne automatiquement
        le fichier physique après l’upload.
        """
        super().save(*args, **kwargs)
        self.resize_image()
