import locale
from django import template

register = template.Library()

# Forcer la locale française (utile si ton système est en anglais)
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error:
    # fallback si la locale n'est pas dispo
    pass

@register.filter
def format_date(value):
    """
    Affiche la date au format : 12:02, 17 Septembre 2025
    """
    if not value:
        return ""
    return value.strftime("%H:%M, %d %B %Y")  # %B = mois complet

@register.filter
def classname(obj):
    """
    Retourne le nom de la classe d’un objet (ex: Review, Ticket)
    """
    return obj.__class__.__name__
