from ..models import Animal

from django import template

register = template.Library()

@register.simple_tag
def list_animal_types():
    pet_type_list = []
    for type_code, pet_type in Animal.ANIMAL_TYPE_CHOICES:
        URL = f"feeding_entry_{type_code}"
        text = f"{pet_type} Feeding"
        pet_type_list.append((text, URL))
    return pet_type_list

