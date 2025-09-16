from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        required=True,
        label="Note"
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
        }
        widgets = {
            'headline': forms.TextInput(attrs={
                'placeholder': 'Titre de la critique',
                'class': 'form-control',
                'required': True
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Écrivez votre commentaire...',
                'class': 'form-control',
                'rows': 5,
                'required': True
            }),
        }
