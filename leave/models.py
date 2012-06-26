from django.db import models
from django.contrib.auth.models import User
#from time import gmtime, strftime
from django.template.defaultfilters import date as _date


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

class Day(models.Model):
    leave_date = models.DateField('leave date')
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ("leave_date", "user"),

    def __unicode__(self):
        return _date(self.leave_date, "D d b Y")
