"""
Django Admin configuration
"""
from django.contrib import admin

from .models import Animal, SnakeFeeding, GeckoFeeding, AnimalCleaning, AnimalHealth
from .models import Snake, Gecko

admin.site.register(Snake)
admin.site.register(Gecko)
admin.site.register(SnakeFeeding)
admin.site.register(GeckoFeeding)
admin.site.register(AnimalCleaning)
admin.site.register(AnimalHealth)
