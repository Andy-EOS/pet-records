from datetime import date, timedelta
from django.test import TestCase

from .models import Snake
from .models import AnimalHealth

from . import test_helpers
"""

LEAVE THIS TEST HERE BUT START WRITING THE REST IN REVERSE ORDER.
SHOULD BE EASIER AS THE Snake and Gecko classes rely heavily on all the others
for their methods to work properly.

class SnakeTests(TestCase):

    def test_creation(self):

        snake = Snake(animal_name="test animal"
        ,animal_dob=date.today() - timedelta(days=3650)
        ,cleaning_frequency=5
        ,_type='SN'
        ,feeding_frequency=12)
        snake.save()

        test_snake = Snake.objects.all()[0]

        self.assertEqual(snake.animal_name, test_snake.animal_name)
        self.assertEqual(snake.animal_dob, test_snake.animal_dob)
        self.assertEqual(snake.cleaning_frequency, test_snake.cleaning_frequency)
        self.assertEqual(snake._type, test_snake._type)
        self.assertEqual(snake.feeding_frequency, test_snake.feeding_frequency)


"""
class AnmialHealthTests(TestCase):

    def test_creation(self):

        stored_healths = test_helpers.create_test_animal_health_list(100)
        test_healths = list(AnimalHealth.objects.all())

        for stored, test, in zip(stored_healths, test_healths):
            self.assertEqual(stored.animal, test.animal)
            self.assertEqual(stored.date, test.date)
            self.assertEqual(stored.weight, test.weight)
            self.assertEqual(stored.food_regurgitated, test.food_regurgitated)
            self.assertEqual(stored.shed, test.shed)
            self.assertEqual(stored.food_refused, test.food_refused)
            self.assertEqual(stored.comments, test.comments)


