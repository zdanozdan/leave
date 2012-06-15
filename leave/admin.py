#custom models
from leave.models import UserProfile
from leave.models import Day
from leave.models import Status
#
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(Day)
admin.site.register(Status)
