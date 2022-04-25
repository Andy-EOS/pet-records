from django.core.management.base import BaseCommand, CommandError
from records.models import Snake, Gecko, Animal
from django.core.mail import send_mail
from datetime import date

class Command(BaseCommand):


    
    def handle(self, *args, **options):

        animals = list(Snake.objects.all()) + list(Gecko.objects.all())
        feeding_text = []
        cleaning_text = []
        for animal in animals:
            if animal.get_feeding_due_in() < 2:
                feeding_text.append(f"{animal.animal_name} {animal.get_feeding_due()}")

            if animal.get_full_clean_due_in() < 7:
                cleaning_text.append(f"{animal.animal_name} full clean {animal.get_full_clean_due()}")

            else:

                if animal.get_spot_clean_due_in() < 2:
                    cleaning_text.append(f"{animal.animal_name} spot clean {animal.get_spot_clean_due()}")


        email_body = ""

        if feeding_text:
            email_body = "The following feeding is due:\n"
            for text in feeding_text:
                email_body = email_body + text + "\n"
            email_body = email_body + "\n\n"

        if cleaning_text:
            email_body = email_body + "The following cleaning is due:\n"
            for text in cleaning_text:
                email_body = email_body + text + "\n"

        if feeding_text or cleaning_text:
            td = date.today()
            d = str(td.day).rjust(2,'0')
            m = str(td.month).rjust(2,'0')
            y = str(td.year).rjust(4,'0')
            feeding_due_date_text = f"{d}/{m}/{y}"

            subject = f"Pet Reminders: {d}/{m}/{y}"

            send_mail(
                subject,
                email_body,
                'autoemails@theedgeofsanity.org.uk',
                ['andy@theedgeofsanity.org.uk'],
                fail_silently=False,
            )
