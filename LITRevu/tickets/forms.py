from django import forms
from .models import Ticket, Image

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'type']
        labels = {
            'title': 'Titre',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Titre du Livre/Article',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Décrivez votre Livre/Article...',
                'class': 'form-control',
                'rows': 5
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }