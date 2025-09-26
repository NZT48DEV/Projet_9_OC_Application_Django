"""
Formulaires pour l'application d'authentification.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription utilisateur.

    Hérite de UserCreationForm et personnalise :
    - Suppression des labels et textes d’aide.
    - Ajout de classes Bootstrap pour le style.
    - Ajout de placeholders explicites.
    """

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec des styles et placeholders personnalisés."""
        super().__init__(*args, **kwargs)

        # Supprimer labels et help_text + personnaliser widgets
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].label = ""
            self.fields[field_name].widget.attrs.update(
                {"class": "form-control mx-auto", "style": "max-width: 300px;"}
            )

        # Ajout des placeholders
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "Nom d’utilisateur"
        self.fields["password1"].widget.attrs["placeholder"] = "Mot de passe"
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "Confirmer mot de passe"


class CustomeAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé.

    Hérite de AuthenticationForm et personnalise :
    - Suppression des labels.
    - Ajout de classes Bootstrap pour le style.
    - Ajout de placeholders explicites.
    """

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec placeholders et styles Bootstrap."""
        super().__init__(*args, **kwargs)

        # Suppression des labels
        self.fields["username"].label = ""
        self.fields["password"].label = ""

        # Personnalisation des widgets
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Nom d’utilisateur",
                "class": "form-control w-100",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Mot de passe",
                "class": "form-control w-100",
            }
        )
