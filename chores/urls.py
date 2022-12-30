"""
urls file for the chores module
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enterchore/', views.chore_entry, name='chore_entry'),
    path('enterchore/<int:chore_id>', views.chore_entry, name="edit_chore_entry"),
    path('donetoday/<int:chore_id>', views.chore_done_today, name="enter_done_today"),
]