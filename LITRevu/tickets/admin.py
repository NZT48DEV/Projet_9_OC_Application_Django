"""
Configuration de l’administration Django pour l’application Tickets.
Permet de gérer facilement les tickets et leurs images associées.
"""

from django.contrib import admin

from tickets.models import Image, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuration de l’interface d’administration pour les tickets.
    - Affiche les colonnes principales : id, titre, description, type, auteur,
      image associée et date de création.
    """

    list_display = (
        "id",
        "title",
        "description",
        "type",
        "user",
        "image",
        "time_created",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Configuration de l’interface d’administration pour les images de tickets.
    - Affiche les colonnes principales : id, chemin de l’image, uploader et date.
    """

    list_display = ("id", "image", "uploader", "time_created")
