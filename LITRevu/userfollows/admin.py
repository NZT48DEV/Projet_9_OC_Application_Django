from django.contrib import admin
from .models import UserFollows


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")   # colonnes affichées dans la liste
    search_fields = ("user__username", "followed_user__username")  # barre de recherche
    list_filter = ("user", "followed_user")  # filtres à droite
