from django import forms
from .models import Ticket, Photo

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'type']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Entrez le titre du ticket',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Décrivez votre ressource...',
                'class': 'form-control',
                'rows': 5
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
