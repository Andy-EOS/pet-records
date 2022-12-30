from django.forms import ModelForm, DateInput, Form, DateField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column

from .models import Chore


class DateEntry(DateInput):
    input_type = 'date'

class DateEntryField(DateField):
    widget = DateEntry

class ChoreForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'chore'
        self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Chore
        fields = (
            'chore_name',
            'date_done',
            'frequency',
        )
        widgets = {
            'date_done': DateEntry(),
        }