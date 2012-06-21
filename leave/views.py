import logging,datetime
from calendar import Calendar

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext

from django.core.urlresolvers import reverse

from leave.models import Day
from leave.forms import LeaveForm
from leave.addon import MikranCalendar

#from django.template.defaultfilters import slugify

# Create your views here.

def index(request):
    users = User.objects.all()
    return render_to_response('index.html',{'users': users})

def show_user(request,user_id):

    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.select_related().filter(user_id__exact=user_id)

    cal = MikranCalendar(user_days).formatyear(2012,4)

    return render_to_response('show_user.html',{'users': users,'selected':selected,'user_days':user_days,'cal':mark_safe(cal)})

def plan_days(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.select_related().filter(user_id__exact=user_id)
    cal = MikranCalendar(user_days).formatyear(2012,4)

    if request.method == 'POST': # If the form has been submitted...
        form = LeaveForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            start_date = datetime.date(int(request.POST['first_day_year']),
                                           int(request.POST['first_day_month']),
                                           int(request.POST['first_day_day']))

            end_date = datetime.date(int(request.POST['last_day_year']),
                                         int(request.POST['last_day_month']),
                                         int(request.POST['last_day_day']))

            current = Calendar()

            start_month = int(request.POST['first_day_month'])
            end_month = int(request.POST['last_day_month'])

            for month in range(start_month,end_month+1):
                for day in current.itermonthdates(int(request.POST['first_day_year']),
                                              month):
                    if day >= start_date and day <= end_date:
                            #
                            # create day object and save in db
                            #
                            day = Day(user_id=selected.id,status_id=1,leave_date=day)
                            day.save()
                    
                            
            #display OK message for the user
            messages.add_message(request,messages.INFO, 'Zaplanowano urlop od %s do %s' %(start_date,end_date))

            return render_to_response('show_user.html',{'users': users,'selected':selected,'user_days':user_days,'cal':mark_safe(cal)})
            return HttpResponseRedirect(reverse('leave.views.show_user',args=(selected.id,)))
    else:
        form = LeaveForm()

    return render_to_response('plan_days.html',{'users': users,
                                                'selected':selected,
                                                'user_days':user_days,
                                                'cal':mark_safe(cal),
                                                'form':form},
                              context_instance=RequestContext(request))

def planned_days(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter(user_id__exact=user_id)

    return render_to_response('plan_days.html',{'users': users,'selected':selected,'user_days':user_days},
                              context_instance=RequestContext(request))
    
