# This Python file uses the following encoding: utf-8

import logging,datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.template.defaultfilters import date as _date
from django.db.models.signals import pre_save,post_save,pre_delete
from django.dispatch import receiver
import django.dispatch
from django.core.mail import send_mass_mail

from django.contrib import admin


# Create your models here.

# user profile keep all information we need extra.

class UserProfile(models.Model):
    phone_number = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return self.user.username

class Status(models.Model):
    status = models.CharField(max_length=50, blank=False)

    def __unicode__(self):
        return self.status

#
# Day model support classes
#
class DayQuerySet(QuerySet):
    def filter_user(self,user_id):
        return self.select_related().filter(user_id__exact=user_id)

    def filter_year(self,year='2012'):
        return self.filter(leave_date__year=year)

    def filter_for_delete(self, uid, start_date, end_date):
        return self.filter(user_id=uid).exclude(status__status="Obecny").exclude(status__status="Lekarskie").filter(leave_date__gte = start_date).filter(leave_date__lte = end_date)

    def filter_status(self,status):
        return self.filter(status__status = status)

    def filter_present(self,year='2012'):
        return self.filter_year(year).filter_status("Obecny")

    def filter_sick(self,year='2012'):
        return self.filter_year(year).filter_status("Lekarskie")

    def filter_planned(self,year='2012'):
        return self.filter_year(year).filter_status("Zaplanowany")

    def filter_accepted(self,year='2012'):
        return self.filter_year(year).filter_status("Zaakceptowane")

class DayManager(models.Manager):
    def get_query_set(self):
        return DayQuerySet(self.model)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

class Day(models.Model):
    leave_date = models.DateField('leave date')
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)

    objects = DayManager()

    class Meta:
        unique_together = ("leave_date", "user"),

    def __unicode__(self):
        return _date(self.leave_date, "D d b Y")


class Event(models.Model):
    date = models.DateField('event date')
    message = models.CharField(max_length=200, blank=False)
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return _date(self.date, "D d b Y")

days_planned = django.dispatch.Signal(providing_args=["start","end","user","status","operation"])

@receiver(days_planned, sender=User)
def days_planned_signal_handler(sender, **kwargs):
    event = Event()
    event.date = datetime.datetime.now()
    
    op_message = "zaplanował"
    if kwargs['operation'] == "DEL":
        op_message = "usunął"

    message ="Użytkownik '%s %s' %s dni od %s do %s" % (kwargs['user'].first_name.encode('utf-8'),
                                                        kwargs['user'].last_name.encode('utf-8'), 
                                                        op_message,
                                                        kwargs['start'],
                                                        kwargs['end'])

    event.message=message

    event.status_id = kwargs['status'].id
    event.user_id = kwargs['user'].id
    event.save()

    EMAIL_HOST_USER = "tomasz@mikran.pl"
    EMAIL_HOST_PASSWORD = "ZDanek123"

    datatuple = (
        (message, message + "\r\nOtrzymujesz tą wiadomość jako administrator. Urlop musi być zaakceptowany przez kierownika/administratora \r\n\r\nhttp://urlopy.mikran.com", 'tomasz@mikran.pl', ['tomasz@mikran.pl']),
        #('Potwierdzenie od urlopy.mikran.com', message + "\r\nOtrzymujesz tą wiadomość jako potwierdzenie. Urlop musi być zaakceptowany przez kierownika/administratora \r\n\r\nhttp://urlopy.mikran.com", 'tomasz@mikran.pl', [kwargs['user'].email]),
        )

    send_mass_mail(datatuple,auth_user=EMAIL_HOST_USER, auth_password=EMAIL_HOST_PASSWORD)

@receiver(pre_save, sender=Day)
def day_save_signal_handler(sender, **kwargs):
    event = Event()
    event.date = datetime.datetime.now()
    event.message="Użytkownik %s %s wykonał operację o statusie: %s" % (kwargs['instance'].user.first_name.encode('utf-8'),
                                                                        kwargs['instance'].user.last_name.encode('utf-8'), 
                                                                        kwargs['instance'].status)
    event.status_id=kwargs['instance'].status_id
    event.user_id = kwargs['instance'].user_id
    event.save()
