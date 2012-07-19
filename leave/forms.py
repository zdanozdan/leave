# This Python file uses the following encoding: utf-8

import datetime,logging
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from django.forms.fields import *
#from django.forms.extras.widgets import SelectDateWidget,Select,HiddenInput
from django.forms.extras.widgets import *
from django.contrib.admin import widgets                                       

from leave.models import *

SICK_CHOICES = (('SICK', 'Lekarskie'),)

PRESENT_CHOICES = (('PRESENT', 'Obecny'),
                   ('SICK', 'Lekarskie'),
                   )

YEAR_CHOICES = ('2012', '2013')
STATUS_CHOICES = (('PLANNED', 'Zaplanowany'),
                  ('ACCEPTED', 'Zaakceptowany'),
                  ('REJECTED', 'Odrzucony'),
                  ('CANCELLED', 'Rezygnuje z urlopu w tym terminie'))


class SinglePresentForm(ModelForm):
    leave_date = forms.DateField(widget=SelectDateWidget(years=YEAR_CHOICES),label='Zgłaszam obecność w dniu')
    status = forms.ModelChoiceField(empty_label=None,queryset=Status.objects.filter(status__in=[item for tuple in PRESENT_CHOICES for item in tuple]),label="Obecny czy nie ?")
    user = forms.ModelChoiceField(empty_label=None,queryset=User.objects.all(),widget=HiddenInput,label='')

    class Meta:
        model = Day

class PresentForm(SinglePresentForm):
    day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES))


class LeaveForm(forms.Form):
    first_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES),label="Pierwszy dzień urlopu")
    last_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES), label="Ostatni dzień urlopu")
    status = forms.ChoiceField(widget=Select, choices=STATUS_CHOICES)
    message = forms.CharField(widget=forms.Textarea, required=False,label="Wiadomość")

    def clean(self):
        cleaned_data = super(LeaveForm, self).clean()

        start = cleaned_data.get("first_day")
        end = cleaned_data.get("last_day")
        status = cleaned_data.get("status")

        if start > end:
            raise forms.ValidationError("Nie no bez przesady ! Jak tak od tyłu ? Data zakończenia musi byc pózniej :-)")

        if self.isPlanned(status) or self.isSick(status) or self.isPresent(status):
            cnt = Day.objects.filter(user_id=self.data['user_id']).filter(leave_date__gte = start).filter(leave_date__lte = end).count();
            if cnt > 0:
                raise forms.ValidationError("W tym terminie juz zaplanowales jakieś dni !")

        if self.isAccepted(status):
            u = User.objects.get(id=self.data['user_id'])
            if u.is_superuser == False:
                raise forms.ValidationError("Sorry ale tylko chief może zaakceptować Twój urlop. Kup piwo i spróbuj ponownie.")

        # Always return the full collection of cleaned data.
        return cleaned_data

    def translateChoice(self,choice):
        return [i[1] for i in STATUS_CHOICES+PRESENT_CHOICES if choice in i].pop()

    def isSick(self,choice):
        return "SICK" in choice

    def isPlanned(self,choice):
        return "PLANNED" in choice

    def isAccepted(self,choice):
        return "ACCEPTED" in choice
    
    def isRejected(self,choice):
        return "REJECTED" in choice

    def isPresent(self,choice):
        return "PRESENT" in choice

    def isCancelled(self,choice):
        return "CANCELLED" in choice

class SickForm(LeaveForm):
    first_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES),label="Pierwszy dzień zwolnienia")
    last_day = forms.DateField(initial=datetime.date.today,widget=SelectDateWidget(years=YEAR_CHOICES), label="Ostatni dzień zwolnienia")
    status = forms.ChoiceField(widget=Select, choices=SICK_CHOICES)
