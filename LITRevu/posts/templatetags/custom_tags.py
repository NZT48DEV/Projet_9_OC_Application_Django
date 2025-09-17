from django import template

register = template.Library()

@register.filter
def classname(obj):
    """Retourne le nom de la classe de l'objet"""
    return obj.__class__.__name__
