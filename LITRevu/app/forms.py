from django import forms
from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.App
        fields = ['title', 'description']