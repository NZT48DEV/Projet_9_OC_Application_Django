"""
Configuration de l'application Posts.
"""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Configuration de l'app Django 'posts'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"
    verbose_name = "Posts"
