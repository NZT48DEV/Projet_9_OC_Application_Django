from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # colonnes affichées dans la liste
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    # champs de recherche
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # ordre d’affichage par défaut
    ordering = ('username',)

    # organisation des champs dans les formulaires d’édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Infos personnelles', {'fields': ('first_name', 'last_name', 'email', 'profile_photo', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # organisation des champs dans le formulaire d’ajout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profile_photo', 'role', 'is_staff', 'is_active'),
        }),
    )
