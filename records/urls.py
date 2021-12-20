"""
urls file for the records module
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('editanimal/SN/<int:animal_id>', views.snake_entry, name = 'edit_animal_entry_SN'),
    path('editanimal/GK/<int:animal_id>', views.gecko_entry, name = 'edit_animal_entry_GK'),
    path('enterfeeding/SN/', views.snake_feeding_entry, name='feeding_entry_SN'),
    path('enterfeeding/GK/', views.gecko_feeding_entry, name='feeding_entry_GK'),
    path('editfeeding/SN/<int:feeding_id>', views.snake_feeding_entry, name="edit_feeding_entry_SN"),
    path('editfeeding/GK/<int:feeding_id>', views.gecko_feeding_entry, name="edit_feeding_entry_GK"),
    path('entercleaning', views.cleaning_entry, name='cleaning_entry'),
    path('editcleaning/<int:cleaning_id>', views.cleaning_entry, name='edit_cleaning_entry'),
    path('enterhealth', views.healthy_entry, name='health_entry'),
    path('edithealth/<int:health_id>', views.healthy_entry, name='edit_health_entry'),
    path('viewfeeding/', views.feeding_records, name='feeding_records'),
    path('viewcleaning/', views.cleaning_records, name='cleaning_records'),
    path('viewhealth', views.health_records, name='health_records'),
    path('weightsGraph', views.weights_graph, name='weights_graph'),
]
