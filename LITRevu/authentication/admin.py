"""
Configuration de l'administration Django pour l'application Authentication.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'interface d'administration pour le modèle User personnalisé.

    - Affiche des colonnes supplémentaires (profile_photo inclus dans les formulaires).
    - Ajoute filtres, recherche et organisation claire des champs.
    """

    # Colonnes affichées dans la liste des utilisateurs
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Champs de recherche
    search_fields = ("username", "email", "first_name", "last_name")

    # Ordre d’affichage par défaut
    ordering = ("username",)

    # Organisation des champs dans les formulaires d’édition
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Infos personnelles",
            {"fields": ("first_name", "last_name", "email", "profile_photo")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Organisation des champs dans le formulaire d’ajout
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "profile_photo",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
