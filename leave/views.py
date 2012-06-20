from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from leave.models import Day
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
