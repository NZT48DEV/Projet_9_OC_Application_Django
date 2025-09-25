"""
Vues de l'application d'authentification.
Gère la connexion, la déconnexion et l'inscription des utilisateurs.
"""

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from . import forms
from .forms import CustomeAuthenticationForm


def logout_user(request):
    """
    Déconnecte l'utilisateur et redirige vers la page d'accueil (welcome).
    """
    logout(request)
    return redirect("welcome")


def signup_page(request):
    """
    Gère l'inscription d'un nouvel utilisateur.

    - Si l'utilisateur est déjà connecté → redirige vers le flux.
    - Si la requête est POST et valide → enregistre l'utilisateur,
      le connecte automatiquement et redirige vers la page définie
      par `LOGIN_REDIRECT_URL`.
    """
    if request.user.is_authenticated:
        return redirect("home")

    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connexion automatique après inscription
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/signup.html", {"form": form})


class CustomLoginView(LoginView):
    """
    Vue personnalisée pour la connexion utilisateur.
    - Utilise un template d'accueil (`welcome.html`).
    - Formulaire de connexion personnalisé (`CustomeAuthenticationForm`).
    - Redirige les utilisateurs déjà connectés.
    """

    template_name = "authentication/welcome.html"
    authentication_form = CustomeAuthenticationForm
    redirect_authenticated_user = True
