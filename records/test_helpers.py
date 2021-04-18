from .models import Animal, Snake, Gecko
from .models import AnimalHealth
from datetime import date, timedelta
import random
import string

def random_string(length):
    """
    Retrun a random string of the given length.
    """
    output = ""

    for _ in range(length):
        output = output + random.choice(string.ascii_letters)

    return output

def random_date(start_year,end_year):
    """
    Retrun a random date in the given range of years.
    """
    start = date(start_year,1,1)
    end = date(end_year,12,31)
    diff = (end - start).days
    return start + timedelta(days=random.randint(0,diff))

def create_snake():
    snake = Snake(
    animal_name=f"Random name: {random_string(5)}"
    ,animal_dob=random_date(2000,2005)
    ,cleaning_frequency=random.randint(1,10)
    ,_type='SN'
    ,feeding_frequency=random.randint(1,25)
    )
    snake.save()
    return snake

def create_gecko():
    gecko = Gecko(
    animal_name=random_string(10)
    ,animal_dob=random_date(2000,2005)
    ,cleaning_frequency=random.randint(1,10)
    ,_type='GK'
    ,feeding_day = random.randint(0,6)
    ,feedings_started = random_date(2006,2007)
    )
    gecko.save()
    return gecko

def create_random_animal():

    selection = [create_snake, create_gecko]
    return random.choice(selection)()

def create_test_animal_health(animal=None):
    if not animal:
        animal = create_random_animal()

    health = AnimalHealth(
    animal=animal
    ,date = random_date(2010,2015)
    ,weight = random.randint(0,1000)
    ,food_regurgitated = random.choice([True,False])
    ,shed = random.choice([True,False])
    ,food_refused = random.choice([True,False])
    ,comments = f"The following is a random string to alter each test descritpion: {random_string(20)}"
    )
    health.save()
    return health

def create_test_animal_health_list(num):
    healths = []

    for _ in range(num):
        healths.append(create_test_animal_health())

    return healths


