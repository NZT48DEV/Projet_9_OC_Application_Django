from django.conf import settings
from django.db import models
from PIL import Image as Img


class Image(models.Model):
    image = models.ImageField()
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

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('BOOK', 'Livre'),
        ('ARTICLE', 'Article'),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='BOOK')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.get_type_display()})'