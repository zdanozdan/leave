from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile keep all information we need extra.

class UserProfile(models.Model):
    phone_number = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, unique=True)

class Status(models.Model):
    status = models.CharField(max_length=50, blank=False)

class Day(models.Model):
    leave_date = models.DateTimeField('leave date')
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
