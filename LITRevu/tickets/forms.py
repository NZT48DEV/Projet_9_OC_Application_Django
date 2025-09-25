"""
Formulaires de l’application Tickets :
- TicketForm : création / modification de tickets.
- ImageForm  : upload d’une image associée à un ticket.
"""

from django import forms
from .models import Ticket, Image


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un ticket.
    Inclut le titre, la description et le type (Livre ou Article).
    """
    class Meta:
        model = Ticket
        fields = ["title", "description", "type"]
        labels = {
            "title": "Titre",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Titre du Livre/Article",
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Décrivez votre Livre/Article...",
                "class": "form-control",
                "rows": 5,
            }),
            "type": forms.Select(attrs={"class": "form-select"}),
        }


class ImageForm(forms.ModelForm):
    """
    Formulaire pour uploader une image associée à un ticket.
    Utilise un champ FileInput stylisé avec Bootstrap.
    """
    class Meta:
        model = Image
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
