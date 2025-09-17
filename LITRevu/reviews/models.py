from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

class Review(models.Model):
    ticket = models.ForeignKey(to='tickets.Ticket', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=8192, blank=True)
    headline = models.CharField(max_length=128)
    time_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.headline} - {self.rating}/5 par {self.user.username}"
