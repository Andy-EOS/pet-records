"""
Django Admin configuration
"""
from django.contrib import admin

from .models import Animal, SnakeFeeding, AnimalCleaning, AnimalHealth
from .models import Snake

admin.site.register(Snake)
admin.site.register(SnakeFeeding)
admin.site.register(AnimalCleaning)
admin.site.register(AnimalHealth)
