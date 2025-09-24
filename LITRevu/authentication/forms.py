from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supprimer labels et help_text
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].label = ""

            # Ajouter form-control à chaque champ
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control mx-auto',
                'style': 'max-width: 300px;'
            })

        # Ajouter placeholders
        self.fields["username"].widget.attrs["placeholder"] = "Nom d’utilisateur"
        self.fields["password1"].widget.attrs["placeholder"] = "Mot de passe"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirmer mot de passe"


class CustomeAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retirer les labels
        self.fields['username'].label = ""
        self.fields['password'].label = ""

        # Ajouter des placeholders
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nom d’utilisateur',
            'class': 'form-control w-100'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Mot de passe',
            'class': 'form-control w-100'
        })