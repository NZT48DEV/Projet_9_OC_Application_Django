from django.conf import settings
from django.db import models
from PIL import Image as Img


class Ticket(models.Model):
    TYPE_CHOICES = [
        ('', 'Choisissez un type'),  # valeur vide affichée en premier
        ('BOOK', 'Livre'),
        ('ARTICLE', 'Article'),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        blank=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'


class Image(models.Model):
    image = models.ImageField()
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="image",
        null=True,     
        blank=True
    )
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def __str__(self):
        return f'{self.image}'

    def resize_image(self):
        image = Img.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
