from django.forms import ModelForm, DateInput, Form, DateField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column

from .models import SnakeFeeding, GeckoFeeding, AnimalCleaning, AnimalHealth
from .models import Animal, Snake, Gecko

class DateEntry(DateInput):
    input_type = 'date'

class DateEntryField(DateField):
    widget = DateEntry

class SnakeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'snake-entry'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))


    class Meta:
        model = Snake
        fields = (
            'animal_name',
            'animal_dob',
            'cleaning_frequency',
            'spot_cleaning_frequency',
            'feeding_frequency',
        )
        widgets = {
            'animal_dob': DateEntry(),
        }

class GeckoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'gecko-entry'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Gecko
        fields = (
            'animal_name',
            'animal_dob',
            'cleaning_frequency',
            'spot_cleaning_frequency',
            'feeding_day',
            'feeding_day_2',
        )
        widgets = {
            'animal_dob': DateEntry(),
            'feedings_started': DateEntry(),
        }

class SnakeFeedingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'snake-feeding'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = SnakeFeeding
        fields = (
            'animal',
            'feeding_date',
            'type_of_food',
            'quantity_fed',
        )
        widgets = {
            'feeding_date': DateEntry(),
        }

class GeckoFeedingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'gecko-feeding'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = GeckoFeeding
        fields = (
            'animal',
            'feeding_date',
            'type_of_food',
            'coating',
            'quantity_given',
            'quantity_eaten',
        )
        widgets = {
            'feeding_date': DateEntry(),
        }

class AnimalCleaningForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'animal-cleaning'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = AnimalCleaning
        fields = (
            'animal',
            'date_cleaned',
            'type_of_clean',
        )
        widgets = {
            'date_cleaned': DateEntry(),
        }

class AnimalHealthForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'animal-health'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = AnimalHealth
        fields = (
            'animal',
            'date',
            'weight',
            'shed',
            'food_regurgitated',
            'food_refused',
            'comments',
        )
        widgets = {
            'date': DateEntry(),
        }

class CleaningFilterForm(Form):
    names_list = []
    #names_list = [('Vivian','Vivian'),('Red','Red'),('Lola','Lola')]
    #for name in list(map(lambda animal: animal.animal_name, Animal.objects.all())):
    #    names_list.append((name, name))
    name = forms.MultipleChoiceField(choices=names_list, widget=forms.CheckboxSelectMultiple(), initial=names_list,required=False)
    date_from = DateEntryField(required=False)
    date_to = DateEntryField(required=False)
    clean_type = forms.MultipleChoiceField(choices=AnimalCleaning.CLEANING_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'health-filter'
        self.helper.form_class = 'blueForms'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('date_from'),
                    Column('date_to'),
                    Column('name'),
                    Column('clean_type'),
                    Column(
                        Row(
                            ButtonHolder(
                                Submit('submit', 'Filter'),
                            )
                        ),
                    )
                )
            )
        )

    class Meta:

        fields = (
            'name',
            'date_from',
            'date_to',
            'clean_type',
        )
        widgets = {
            'date_from': DateEntry(),
            'date_to': DateEntry(),
        }

class BasicFilterForm(Form):
    names_list = []
    #names_list = [('Vivian','Vivian'),('Red','Red'),('Lola','Lola')]
    #for name in list(map(lambda animal: animal.animal_name, Animal.objects.all())):
    #    names_list.append((name, name))
    name = forms.MultipleChoiceField(choices=names_list, widget=forms.CheckboxSelectMultiple(), initial=names_list,required=False)
    #name = forms.ModelChoiceField(queryset=Animal.objects.all())

    date_from = DateEntryField(required=False)
    date_to = DateEntryField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'basic-filter'
        self.helper.form_class = 'blueForms'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('date_from'),
                    Column('date_to'),
                    Column('name'),
                    Column(
                        Row(
                            ButtonHolder(
                                Submit('submit', 'Filter')
                            )
                        )
                    )
                )
            )
        )

    class Meta:

        fields = (
            'name',
            'date_from',
            'date_to',
        )
        widgets = {
            'date_from': DateEntry(),
            'date_to': DateEntry(),
        }
