from datetime import date, timedelta
from django.test import TestCase

from .models import Snake

class SnakeTests(TestCase):

    def test_creation(self):

        snake = Snake(animal_name="test animal"
        ,animal_dob=date.today() - timedelta(days=3650)
        ,cleaning_frequency=5
        ,_type='SN'
        ,feeding_frequency=12)
        snake.save()

        