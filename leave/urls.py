from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('leave.views',
    url(r'^$','index',name='index'),
    url(r'^show/(?P<user_id>\d+)/user/$', 'show_user', name="show_user"),
    url(r'^plan/(?P<user_id>\d+)/user/$', 'plan_days', name="plan_days"),
    url(r'^planned/(?P<user_id>\d+)/user/$', 'planned_days', name="planned_days"),
)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)



