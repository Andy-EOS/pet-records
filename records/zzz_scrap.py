import random
import string
from datetime import date, timedelta


def return_zero():
    return 0

def return_one():
    return 1

def return_random():

    selection = [return_zero, return_one]
    #return selection[random.randint(0,len(selection)-1)]()
    return random.choice(selection)()

for _ in range(20):
    print(return_random())

