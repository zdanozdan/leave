import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets                                       


YEAR_CHOICES = ('2012', '2013')

class LeaveForm(forms.Form):
    #first_day = forms.DateField(initial=datetime.date.today,widget=widgets.AdminDateWidget)
    first_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    last_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))
    message = forms.CharField()

