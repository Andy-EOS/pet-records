from django.db import models
from datetime import timedelta, date

# Create your models here.

class Chore(models.Model):

    chore_name = models.CharField(max_length=200)
    date_done = models.DateField('date done')
    frequency = models.IntegerField(default=7)

    def __str__(self):
        return self.chore_name

    def get_date_due(self):
        return self.date_done + timedelta(days=self.frequency)

    def get_due_in_days(self):
        return (self.get_date_due() - date.today()).days