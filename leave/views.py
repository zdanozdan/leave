# This Python file uses the following encoding: utf-8

import logging,datetime
from calendar import Calendar

from collections import defaultdict

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import redirect

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from leave.models import *
from leave.forms import *

from leave.addon import MikranCalendar
from leave.decorators import user_allowed

from django.http import HttpResponseRedirect
from functools import wraps

# Create your views here.

@login_required
def index(request):
    users = User.objects.all()
    user_days = Day.objects.select_related()
    cal = MikranCalendar(user_days).formatyear(2012,4)

    return render_to_response('index.html',{'users': users,'user_days':user_days,'cal':mark_safe(cal)},
                              context_instance=RequestContext(request))

@login_required
def show_user(request,user_id):
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter_user(user_id)
    cal = MikranCalendar(user_days,selected.id)

    return render_to_response('show_user.html',{'days_present': user_days.filter_present().count(),
                                                'days_sick':user_days.filter_sick().count(),
                                                'days_planned':user_days.filter_planned().count(),
                                                'days_accepted':user_days.filter_accepted().count(),
                                                'selected':selected,
                                                'user_days':user_days,
                                                'cal':mark_safe(cal.formatyear(2012,4))
                                                },
                              context_instance=RequestContext(request))

@login_required
def show_present(request,year,month,day):
    users = User.objects.all()
    user_days = Day.objects.select_related()
    cal = MikranCalendar(user_days)

    url_day = datetime.date(int(year),int(month),int(day))
    present_days = Day.objects.select_related().filter(leave_date = url_day)

    return render_to_response('show_present.html',{'users': users,
                                                   'cal':mark_safe(cal.formatyear(2012,4)),
                                                   'year':year, 
                                                   'month':month, 
                                                   'day':day, 
                                                   'statuses':cal.group_days_by_statuses(present_days)
                                                   },
                              context_instance=RequestContext(request))

@login_required
@user_allowed
def single_present(request,user_id,year,month,day):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter_user(user_id)

    url_day = datetime.date(int(year),int(month),int(day))
    present_days = Day.objects.select_related().filter(leave_date = url_day)

    #check if logged useed already used that day, if no form will appear, otherwise warning will be shown
    user_day = user_days.filter(leave_date = url_day)
    if user_day:
        user_day = user_day[0]

    form = SinglePresentForm(instance=Day(user_id=selected.id,status_id=Status.objects.get(status="Obecny").id,leave_date=url_day))

    cal = MikranCalendar(user_days,selected.id)

    if request.method == 'POST': # If the form has been submitted...
        form = SinglePresentForm(request.POST, instance=Day(user_id=selected.id,status_id=Status.objects.get(status="Obecny").id,leave_date=url_day))
        if form.is_valid(): # All validation rules pass
            #display OK message for the user
            form.save()
            messages.add_message(request,messages.INFO, 'Ten dzień (%s) jest już zarezerwowany' %(url_day))
            return HttpResponseRedirect(reverse('leave.views.show_user',args=(selected.id,)))
        

    return render_to_response('present.html',{'users': users,
                                              'selected':selected,
                                              'user_days':user_days,
                                              'user_day':user_day,
                                              'days_present': user_days.filter_present().count(),
                                              'days_sick':user_days.filter_sick().count(),
                                              'days_planned':user_days.filter_planned().count(),
                                              'days_accepted':user_days.filter_accepted().count(),
                                              'selected':selected,
                                              'cal':mark_safe(cal.formatyear(2012,4)),
                                              'form':form, 
                                              'year':year, 
                                              'month':month, 
                                              'day':day, 
                                              'statuses':cal.group_days_by_statuses(present_days)
                                              },
                              context_instance=RequestContext(request))

@login_required
def present(request,user_id):
    form = PresentForm()
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter_user(user_id)

    cal = MikranCalendar(user_days).formatyear(2012,4)

    return render_to_response('present.html',{'users': users,'selected':selected,'user_days':user_days,'cal':mark_safe(cal),'form':form},
                              context_instance=RequestContext(request))

@login_required
@user_allowed
def sick(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter_user(user_id)
    cal = MikranCalendar(user_days).formatyear(2012,4)

    if request.method == 'POST': # If the form has been submitted...
        form = SickForm(dict(request.POST.items() + {'user_id':selected.id}.items())) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            start_date = datetime.date(int(request.POST['first_day_year']),
                                       int(request.POST['first_day_month']),
                                       int(request.POST['first_day_day']))
            
            end_date = datetime.date(int(request.POST['last_day_year']),
                                     int(request.POST['last_day_month']),
                                     int(request.POST['last_day_day']))

            start_month = int(request.POST['first_day_month'])
            end_month = int(request.POST['last_day_month'])

            status_obj = Status.objects.get(status=form.translateChoice(request.POST['status']));

            days = []
            current = Calendar()
            for month in range(start_month,end_month+1):
                for day in current.itermonthdates(int(request.POST['first_day_year']),
                                                  month):
                    if day >= start_date and day <= end_date:
                        if day.isoweekday() < 6:
                            if not day in days:
                                days.append(day)

            #build list of objects for bulk create
            Day.objects.bulk_create([Day(user_id=selected.id,status_id=status_obj.id,leave_date=day) for day in days])
            #send bulk sick days create signal
            days_planned.send(sender=User, user=selected, status=status_obj, start=start_date, end=end_date, operation="SICK".encode('utf-8'))

            #display OK message for the user
            messages.add_message(request,messages.INFO, 'Zgłosiłeś zwolnienie lekarskie od %s do %s' %(start_date,end_date))

            return HttpResponseRedirect(reverse('leave.views.show_user',args=(selected.id,)))
    else:
        form = SickForm()
        
    return render_to_response('sick_days.html',{'users': users,
                                                'selected':selected,
                                                'user_days':user_days,
                                                'cal':mark_safe(cal),
                                                'days_present': user_days.filter_present().count(),
                                                'days_sick':user_days.filter_sick().count(),
                                                'days_planned':user_days.filter_planned().count(),
                                                'days_accepted':user_days.filter_accepted().count(),
                                                'form':form},
                              context_instance=RequestContext(request))


@login_required
@user_allowed
def plan_days(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter_user(user_id)
    cal = MikranCalendar(user_days).formatyear(2012,4)

    if request.method == 'POST': # If the form has been submitted...
        form = LeaveForm(dict(request.POST.items() + {'user_id':selected.id}.items())) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            start_date = datetime.date(int(request.POST['first_day_year']),
                                       int(request.POST['first_day_month']),
                                       int(request.POST['first_day_day']))
            
            end_date = datetime.date(int(request.POST['last_day_year']),
                                     int(request.POST['last_day_month']),
                                     int(request.POST['last_day_day']))

            start_month = int(request.POST['first_day_month'])
            end_month = int(request.POST['last_day_month'])

            status_obj = Status.objects.get(status=form.translateChoice(request.POST['status']));

            if form.isCancelled(request.POST['status']):
                Day.objects.filter_for_delete(selected.id, start_date, end_date).delete()
                #
                #send signal for bulk operation
                days_planned.send(sender=User, user=selected, status=status_obj, start=start_date, end=end_date, operation="DEL")

            elif form.isPlanned(request.POST['status']):
                days = []
                current = Calendar()
                for month in range(start_month,end_month+1):
                    for day in current.itermonthdates(int(request.POST['first_day_year']),
                                                      month):
                        if day >= start_date and day <= end_date:
                            if day.isoweekday() < 6:
                                if not day in days:
                                    days.append(day)

                #build list of objects for bulk create
                Day.objects.bulk_create([Day(user_id=selected.id,status_id=status_obj.id,leave_date=day) for day in days])
                #send bulk days create signal
                days_planned.send(sender=User, user=selected, status=status_obj, start=start_date, end=end_date, operation="PLAN".encode('utf-8'))

            else:
                Day.objects.filter(user_id=selected.id,
                                   leave_date__gte = start_date,
                                   leave_date__lte = end_date).update(status=status_obj.id)
                            
            #display OK message for the user
            messages.add_message(request,messages.INFO, 'Zaplanowano urlop od %s do %s' %(start_date,end_date))

            return HttpResponseRedirect(reverse('leave.views.show_user',args=(selected.id,)))
    else:
        form = LeaveForm()

    return render_to_response('plan_days.html',{'users': users,
                                                'selected':selected,
                                                'user_days':user_days,
                                                'cal':mark_safe(cal),
                                                'days_present': user_days.filter_present().count(),
                                                'days_sick':user_days.filter_sick().count(),
                                                'days_planned':user_days.filter_planned().count(),
                                                'days_accepted':user_days.filter_accepted().count(),
                                                'form':form},
                              context_instance=RequestContext(request))

    
