import datetime,logging
from django import forms
from django.forms.extras.widgets import SelectDateWidget,Select
from django.contrib.admin import widgets                                       


YEAR_CHOICES = ('2012', '2013')
FAVORITE_COLORS_CHOICES = (('1', 'Zaplanowany'),
                           ('2', 'Zaakceptowany'),
                           ('3', 'Odrzucony'),
                           ('4', 'Rezygnuje z urlopu w tym terminie'))

class LeaveForm(forms.Form):
    #first_day = forms.DateField(initial=datetime.date.today,widget=widgets.AdminDateWidget)
    first_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    last_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    status = forms.ChoiceField(widget=Select, choices=FAVORITE_COLORS_CHOICES)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super(LeaveForm, self).clean()

        start = cleaned_data.get("first_day")
        end = cleaned_data.get("last_day")

        logging.debug(cleaned_data.get("first_day") < cleaned_data.get("last_day"))
        logging.debug(end)

        if start > end:
            raise forms.ValidationError("Nie no bez przesady ! Chcesz urlop od tylu ? Data zakonczenia musi byc pozniej :-)")

        # Always return the full collection of cleaned data.
        return cleaned_data

