"""
Formulaires liés aux critiques (reviews).
Permettent la création et la modification des critiques associées aux tickets.
"""

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour la création et la mise à jour des critiques.
    Inclut :
    - un titre (headline),
    - une note (rating),
    - un commentaire (body).
    """

    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        required=True,
        label="Note",
        help_text="Attribuez une note entre 0 et 5"
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
            "headline": "Titre",
            "body": "Commentaire",
        }
        widgets = {
            "headline": forms.TextInput(
                attrs={
                    "placeholder": "Titre de la critique",
                    "class": "form-control",
                    "required": True,
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Écrivez votre critique...",
                    "class": "form-control",
                    "rows": 5,
                    "required": True,
                }
            ),
        }
