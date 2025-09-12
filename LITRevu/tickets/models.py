from django.conf import settings
from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.image}'

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('BOOK', 'Livre'),
        ('ARTICLE', 'Article'),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=5000)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='BOOK')
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'