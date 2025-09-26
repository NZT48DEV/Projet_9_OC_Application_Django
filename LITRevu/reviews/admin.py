"""
Configuration de l'administration Django pour l'application Reviews.
Permet de personnaliser l'affichage et la gestion des critiques dans l'admin.
"""

from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour les critiques."""

    list_display = (
        "id",
        "ticket",
        "rating",
        "user",
        "headline",
        "body",
        "time_created",
    )
    search_fields = ("headline", "body", "user__username")
    list_filter = ("rating", "time_created", "user")
    ordering = ("-time_created",)
