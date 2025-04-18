"""
Django models for the records app
"""
from math import floor, ceil
import json
from datetime import date, timedelta
from django.db import models
from django.utils.timezone import now

def get_next_day(date_, weekday_, weekday2_):
    return_date = date_+ timedelta(days=1)
    loop_count = 0
    while True:
        if return_date.weekday() == weekday_ or return_date.weekday() == weekday2_:
            return return_date
        return_date = return_date + timedelta(days=1)
        loop_count +=1
        if loop_count > 100:
            raise("get_next_day loop counter exceded")

class Animal(models.Model):
    """
    Animal model for basic pet information.
    """
    animal_name = models.CharField(max_length=100)
    animal_dob = models.DateField()

    SNAKE = 'SN'
    ANIMAL_TYPE_CHOICES = [
        (SNAKE, 'Snake'),
    ]

    cleaning_frequency = models.IntegerField("Cleaning frequency (weeks)", default=6)
    spot_cleaning_frequency = models.IntegerField("Spot cleaning frequency (weeks)", default = 2)

    def __str__(self):
        return self.animal_name

 
    def get_animal_name(self):
        return self.animal_name

    def dob_text(self):
        dt = self.animal_dob
        d = str(dt.day).rjust(2,'0')
        m = str(dt.month).rjust(2,'0')
        y = str(dt.year).rjust(4,'0')
        return f"{d}/{m}/{y}"

    def get_last_cleaned(self):
        cleanings = AnimalCleaning.objects.filter(animal=self).order_by('-date_cleaned')[:1]
        if cleanings:
            return cleanings[0].date_cleaned
        else:
            return "No cleaning recorded."

    def get_last_spot_cleaned(self):
        spot_cleanings = AnimalCleaning.objects.filter(animal=self).filter(type_of_clean="SP").order_by('-date_cleaned')[:1]
        if spot_cleanings:
            return spot_cleanings[0].date_cleaned
        else:
            return "No spot cleans recorded."

    def get_last_full_cleaned(self):
       full_cleanings = AnimalCleaning.objects.filter(animal=self).filter(type_of_clean="FU").order_by('-date_cleaned')[:1]
       if full_cleanings:
           return full_cleanings[0].date_cleaned
       else:
           return "No full cleans recorded."

  
    def get_full_clean_due(self):
        if self.get_last_full_cleaned() == "No full cleans recorded.":
            return "No full cleans recorded."
        full_cleaning_due_date = self.get_last_full_cleaned() + timedelta(weeks=self.cleaning_frequency)
        d = str(full_cleaning_due_date.day).rjust(2,'0')
        m = str(full_cleaning_due_date.month).rjust(2,'0')
        y = str(full_cleaning_due_date.year).rjust(4,'0')
        full_cleaning_due_date_text = f"{d}/{m}/{y}"

        full_cleaning_due_in_days = self.get_full_clean_due_in()
        full_cleaning_due_in_weeks = floor(full_cleaning_due_in_days / 7)

        if full_cleaning_due_in_days > 0:
            return f"Due: {full_cleaning_due_date_text} ({full_cleaning_due_in_weeks} weeks)"
        elif full_cleaning_due_in_days < 0:
            return f"Due: {full_cleaning_due_date_text}  (overdue {abs(full_cleaning_due_in_weeks)} weeks)"
        else:
            return "Full Clean due Today."

    def get_spot_clean_due(self):
        if self.get_full_clean_due_in() < self.spot_cleaning_frequency * 7:
            return "Full clean almost due."
        if self.get_last_cleaned() == "No cleaning recorded.":
            return "No cleaning recorded."
        spot_cleaning_due_date = self.get_last_cleaned() + timedelta(weeks=self.spot_cleaning_frequency)
        d = str(spot_cleaning_due_date.day).rjust(2,'0')
        m = str(spot_cleaning_due_date.month).rjust(2,'0')
        y = str(spot_cleaning_due_date.year).rjust(4,'0')
        spot_cleaning_due_date_text = f"{d}/{m}/{y}"

        spot_cleaning_due_in_days = self.get_spot_clean_due_in()

        if spot_cleaning_due_in_days > 0:
            return f"Due: {spot_cleaning_due_date_text} ({spot_cleaning_due_in_days} days)"
        elif spot_cleaning_due_in_days < 0:
            return f"Due: {spot_cleaning_due_date_text}  (overdue {abs(spot_cleaning_due_in_days)} days)"
        else:
            return "Spot Clean due Today."

    def get_full_clean_due_in(self):
        if self.get_last_full_cleaned() == "No full cleans recorded.":
            return 0

        cleaning_due_date = self.get_last_full_cleaned() + timedelta(weeks=self.cleaning_frequency)
        return (cleaning_due_date - date.today()).days

    def get_spot_clean_due_in(self):
        if self.get_last_cleaned() == "No cleaning recorded.":
            return 0

        cleaning_due_date = self.get_last_cleaned() + timedelta(weeks=self.spot_cleaning_frequency)
        return (cleaning_due_date - date.today()).days

class Snake(Animal):

    _type = models.CharField(max_length=2,default='SN')
    feeding_frequency = models.IntegerField("Feeding Frequency (days)", default = 14)

    def __eq__(self, other):
        if type(other) != Snake:
            return False
        if self.animal_name != other.animal_name:
            return False
        if self.animal_dob != other.animal_dob:
            return False
        if self.cleaning_frequency != other.cleaning_frequency:
            return False
        if self._type != other._type:
            return False
        if self.feeding_frequency != other.feeding_frequency:
            return False
        return True

    def get_animal_type(self):
        return self._type

    def table_entry(self):
        feeding_cell_colour = "default"
        spot_clean_cell_colour = "default"
        full_clean_cell_colour = "default"

        feeding_due_in = self.get_feeding_due_in()
        if feeding_due_in > 0:
            feeding_cell_colour = "green"
        if feeding_due_in == 0:
            feeding_cell_colour = "yellow"
        if feeding_due_in < 0:
            feeding_cell_colour = "red"

        spot_clean_due_in = self.get_spot_clean_due_in()
        if spot_clean_due_in > 0:
            spot_clean_cell_colour = "green"
        if spot_clean_due_in == 0:
            spot_clean_cell_colour = "yellow"
        if spot_clean_due_in < 0:
            spot_clean_cell_colour = "red"

        full_clean_due_in = self.get_full_clean_due_in()
        if full_clean_due_in > 0:
            full_clean_cell_colour = "green"
        if full_clean_due_in == 0:
            full_clean_cell_colour = "yellow"
        if full_clean_due_in < 0:
            full_clean_cell_colour = "red"

        return (self.animal_name, self.get_feeding_due, self.get_full_clean_due(), self.get_spot_clean_due(), f"edit_animal_entry_{self._type}", self.id
        , feeding_cell_colour, spot_clean_cell_colour, full_clean_cell_colour)

    def get_last_fed(self):
        feedings = SnakeFeeding.objects.filter(animal=self).order_by('-feeding_date')[:1]
        if feedings:
            return feedings[0].feeding_date
        else:
            return "No feedings recorded."
    
    def get_feeding_due(self):
        if self.get_last_fed() == "No feedings recorded.":
            return "Never fed."
        feeding_due_date = self.get_last_fed() + timedelta(days=self.feeding_frequency)
        d = str(feeding_due_date.day).rjust(2,'0')
        m = str(feeding_due_date.month).rjust(2,'0')
        y = str(feeding_due_date.year).rjust(4,'0')
        feeding_due_date_text = f"{d}/{m}/{y}"

        feeding_due_in = self.get_feeding_due_in()

        if feeding_due_in > 0:
            return f"Due: {feeding_due_date_text} ({feeding_due_in} days)"
        elif feeding_due_in < 0:
            return f"Due: {feeding_due_date_text} (overdue {abs(feeding_due_in)} days)"
        else:
            return "Feeding due Today."

    def get_feeding_due_in(self):
        feeding_due_date = self.get_last_fed() + timedelta(days=self.feeding_frequency)
        return (feeding_due_date - date.today()).days
        


class SnakeFeeding(models.Model):
    """
    Model to handle snake feeding database entries.
    """
    animal = models.ForeignKey(Snake,on_delete=models.CASCADE)
    feeding_date = models.DateField()
    quantity_fed = models.IntegerField(default=1)

    PINKY = 'PK'
    FUZZY = 'FZ'
    SMALL_MOUSE = 'SM'
    MEDIUM_MOUSE = 'MM'
    LARGE_MOUSE = 'LM'
    JUMBO_MOUSE = 'JM'
    RAT_WEANER = 'RW'

    SNAKE_FEEDING_CHOICES = [
        (PINKY, 'Pinkie'),
        (FUZZY, 'Fuzzy'),
        (SMALL_MOUSE, 'Small Mouse'),
        (MEDIUM_MOUSE, 'Medium Mouse'),
        (LARGE_MOUSE, 'Large Mouse'),
        (JUMBO_MOUSE, 'Jumbo Mouse'),
        (RAT_WEANER, 'Rat Weaner'),
    ]
    type_of_food = models.CharField(max_length=2,choices=SNAKE_FEEDING_CHOICES,default=LARGE_MOUSE)

    def __str__(self):
        return f"{self.feeding_date}: {self.animal} was fed {self.quantity_fed} {self.type_of_food}."

    def get_date(self):
        return self.feeding_date
    
    def date_text(self):
        dt = self.feeding_date
        d = str(dt.day).rjust(2,'0')
        m = str(dt.month).rjust(2,'0')
        y = str(dt.year).rjust(4,'0')
        return f"{d}/{m}/{y}"

    def feeding_text(self):
        food_type_text = "ERROR!"
        for food_code, food_type in self.SNAKE_FEEDING_CHOICES:
            if food_code == self.type_of_food:
                food_type_text = food_type
                break
        return f"{self.quantity_fed} {food_type_text}"

    def table_entry(self):
        return (self.date_text(), self.animal.animal_name, self.feeding_text(), f"edit_feeding_entry_{self.animal._type}", self.id)



class AnimalCleaning(models.Model):
    """
    Model to handle animal enclosure cleaning database entries.
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date_cleaned = models.DateField()

    SPOT = 'SP'
    FULL = 'FU'

    CLEANING_TYPE_CHOICES = [
        (SPOT, "Spot Clean"),
        (FULL, "Full Clean"),
    ]
    type_of_clean = models.CharField(max_length=2,choices=CLEANING_TYPE_CHOICES,default=SPOT)

    def date_text(self):
        dt = self.date_cleaned
        d = str(dt.day).rjust(2,'0')
        m = str(dt.month).rjust(2,'0')
        y = str(dt.year).rjust(4,'0')
        return f"{d}/{m}/{y}"

    def get_date(self):
        return self.date_cleaned

    def clean_text(self):
        cleaning_text = "ERROR!"
        for clean_code, clean_text in self.CLEANING_TYPE_CHOICES:
            if self.type_of_clean == clean_code:
                cleaning_text = clean_text
                break
        return cleaning_text

    def table_entry(self):
        return (self.date_text(), self.animal.animal_name, self.clean_text(), f"edit_cleaning_entry", self.id)

class AnimalHealth(models.Model):
    """
    Model to handle the health of an animal.
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.IntegerField("Weight (grams)",blank=True, null=True)
    food_regurgitated = models.BooleanField(default=False)
    shed = models.BooleanField(default=False)
    food_refused = models.BooleanField(default=False)
    comments = models.CharField(max_length=10000,blank=True, null=True)

    def get_date(self):
        return self.date

    def date_text(self):
        dt = self.date
        d = str(dt.day).rjust(2,'0')
        m = str(dt.month).rjust(2,'0')
        y = str(dt.year).rjust(4,'0')
        return f"{d}/{m}/{y}"

    def table_entry(self):
        weight = ""
        if self.weight:
            weight = f"{self.weight}g"

        regurgitated = ""
        if self.food_regurgitated:
            regurgitated = "Regurgitated"

        shed = ""
        if self.shed:
            shed = "Shed"

        refused = ""
        if self.food_refused:
            refused = "Refused Food"

        comments = ""
        if self.comments:
            comments = self.comments

        return (
            self.date_text(),
            self.animal.animal_name,
            weight,
            shed,
            refused,
            regurgitated,
            comments,
            f"edit_health_entry",
            self.id,
            )


