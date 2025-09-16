from django.core.exceptions import ValidationError

def validate_rating(value):
    if value < 0 or value > 5:
        raise ValidationError(f"La note doit être comprise entre 0 et 5. (valeur donnée : {value})")
