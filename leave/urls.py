from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('leave.views',
    url(r'^$','index',name='index'),
    url(r'^show/(?P<user_id>\d+)/user/$', 'show_user', name="show_user"),
    url(r'^plan/(?P<user_id>\d+)/user/$', 'plan_days', name="plan_days"),
    #url(r'^planned/(?P<user_id>\d+)/user/$', 'planned_days', name="planned_days"),
    url(r'^present/(?P<user_id>\d+)/user/$', 'present', name="present"),
    #url(r'^single/present/(?P<user_id>\d+)/user/$', 'single_present', name="single_present"),
    url(r'^zlgos/obecnosc/(?P<user_id>\d+)/w/dniu/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'single_present', name='single_present'),
)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)



