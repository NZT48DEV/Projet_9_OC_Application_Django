from django.contrib import admin
from .models import UserFollows, UserBlock


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user", "created_at")   # affiche aussi la date
    search_fields = ("user__username", "followed_user__username")
    list_filter = ("user", "followed_user", "created_at")    # filtre par date possible
    ordering = ("-created_at",)  # plus récents en premier


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ("user", "blocked_user", "created_at")
    search_fields = ("user__username", "blocked_user__username")
    list_filter = ("user", "blocked_user", "created_at")
    ordering = ("-created_at",)
