"""
Configuration de l’administration Django pour les modèles UserFollows et UserBlock.
Permet de gérer facilement les abonnements et blocages depuis l’interface admin.
"""

from django.contrib import admin
from .models import UserFollows, UserBlock


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """
    Configuration de l’interface d’administration pour les abonnements.
    - Affiche les colonnes : utilisateur, suivi, date de création.
    - Ajoute des filtres et la recherche par username.
    - Trie par date (les plus récents en premier).
    """
    list_display = ("user", "followed_user", "created_at")
    search_fields = ("user__username", "followed_user__username")
    list_filter = ("user", "followed_user", "created_at")
    ordering = ("-created_at",)


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    """
    Configuration de l’interface d’administration pour les blocages.
    - Affiche les colonnes : utilisateur, bloqué, date de création.
    - Ajoute des filtres et la recherche par username.
    - Trie par date (les plus récents en premier).
    """
    list_display = ("user", "blocked_user", "created_at")
    search_fields = ("user__username", "blocked_user__username")
    list_filter = ("user", "blocked_user", "created_at")
    ordering = ("-created_at",)
