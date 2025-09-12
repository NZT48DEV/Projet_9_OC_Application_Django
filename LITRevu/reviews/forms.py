from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'note', 'commentary']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Titre de la critique',
                'class': 'form-control',
                'required': True
            }),
            'note': forms.RadioSelect(choices=Review.NOTE_CHOICES, attrs={
                'required': True
            }),
            'commentary': forms.Textarea(attrs={
                'placeholder': 'Écrivez votre commentaire...',
                'class': 'form-control',
                'rows': 5,
                'required': True
            }),
        }
