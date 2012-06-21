import logging,datetime
from calendar import Calendar

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
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

def showUser(request,user_id):

    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter(user_id__exact=user_id)

    cal = MikranCalendar(user_days).formatyear(2012,4)

    return render_to_response('show_user.html',{'users': users,'selected':selected,'user_days':user_days,'cal':mark_safe(cal)})

def planDays(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter(user_id__exact=user_id)

    if request.method == 'POST': # If the form has been submitted...
        form = LeaveForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logging.debug(request.POST)
            logging.debug(request.POST['first_day_month'])

            start_date = datetime.date(int(request.POST['first_day_year']),
                                           int(request.POST['first_day_month']),
                                           int(request.POST['first_day_day']))

            end_date = datetime.date(int(request.POST['last_day_year']),
                                         int(request.POST['last_day_month']),
                                         int(request.POST['last_day_day']))

            logging.debug(start_date)
            logging.debug(end_date)
            if(start_date < end_date):
                logging.debug("OK")

            cal = Calendar()

            start_month = int(request.POST['first_day_month'])
            end_month = int(request.POST['last_day_month'])

#            for month in range(start_month,end_month):
            for day in cal.itermonthdates(int(request.POST['first_day_year']),
                                          month):
                logging.debug(str(start_date) + ":" + str(day))
                if day >= start_date:
                    logging.debug(str(start_date) + ":!!!!!!!!!!!!!!!!!!!!!" + str(day))
                        #                        if day <= end_date:
    

            d = Day(user_id=1,status_id=1,leave_date=start_date)
            d.save()
            d = Day(user_id=1,status_id=1,leave_date=end_date)
            d.save()
            #selected_choice = p.choice_set.get(pk=request.POST['choice'])

            #logging.debug(reverse('leave.views.planned_days',args=(1,)))
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/leave/planned/'+str(selected.id)+'/user/') # Redirect after POST
            #return HttpResponseRedirect(reverse('leave.views.planned_days',args=(selected.id,)))
    else:
        form = LeaveForm()

    return render_to_response('plan_days.html',{'users': users,'selected':selected,'user_days':user_days,'form':form},
                              context_instance=RequestContext(request))

def planned_days(request,user_id):
    users = User.objects.all()
    selected = User.objects.get(pk=user_id)
    user_days = Day.objects.filter(user_id__exact=user_id)

    return render_to_response('plan_days.html',{'users': users,'selected':selected,'user_days':user_days},
                              context_instance=RequestContext(request))
    
