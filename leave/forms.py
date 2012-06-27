import datetime,logging
from django import forms
from django.forms.extras.widgets import SelectDateWidget,Select
from django.contrib.admin import widgets                                       


YEAR_CHOICES = ('2012', '2013')
STATUS_CHOICES = (('PLANNED', 'Zaplanowany'),
                  ('ACCEPTED', 'Zaakceptowany'),
                  ('REJECTED', 'Odrzucony'),
                  ('CANCELLED', 'Rezygnuje z urlopu w tym terminie'))

class LeaveForm(forms.Form):
    #first_day = forms.DateField(initial=datetime.date.today,widget=widgets.AdminDateWidget)
    first_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    last_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    status = forms.ChoiceField(widget=Select, choices=STATUS_CHOICES)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super(LeaveForm, self).clean()

        start = cleaned_data.get("first_day")
        end = cleaned_data.get("last_day")

        #logging.debug(cleaned_data.get("first_day") < cleaned_data.get("last_day"))
        #logging.debug(end)

        if start > end:
            raise forms.ValidationError("Nie no bez przesady ! Chcesz urlop od tylu ? Data zakonczenia musi byc pozniej :-)")

        # Always return the full collection of cleaned data.
        return cleaned_data

    def translateChoice(self,choice):
        return [i[1] for i in STATUS_CHOICES if choice in i].pop()

    def isPlanned(self,choice):
        return "PLANNED" in choice
    
    def isRejected(self,choice):
        return "REJECTED" in choice

    def isCancelled(self,choice):
        return "CANCELLED" in choice

