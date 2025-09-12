from django.conf import settings
from django.db import models

class Review(models.Model):
    NOTE_CHOICES = [(i, str(i)) for i in range(6)]

    title = models.CharField(max_length=128, blank=False)
    note = models.IntegerField(choices=NOTE_CHOICES, null=False, blank=False)
    commentary = models.CharField(max_length=5000, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.note}/5 par {self.author.username}"