from django.conf import settings
from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class App(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=5000)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)