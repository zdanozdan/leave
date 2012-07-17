#custom models
from leave.models import UserProfile
from leave.models import Day
from leave.models import Status
from leave.models import Event
#
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    list_display = ('date','message','user','status')

class DayAdmin(admin.ModelAdmin):
    list_display = ('leave_date','status','user')
    list_filter = ('user','status')

admin.site.register(UserProfile)
admin.site.register(Day,DayAdmin)
admin.site.register(Status)
admin.site.register(Event,EventAdmin)
