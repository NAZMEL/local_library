from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import DateTimeBaseInput
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = "Enter a date")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if a date isn't in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'
            ))

        return data