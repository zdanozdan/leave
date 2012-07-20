from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('leave.views',
    url(r'^$','index',name='index'),
    url(r'^accounts/profile/$', 'show_profile', name='show_profile'),
    url(r'^(?P<user_id>\d+)/pokaz/pracownika/$', 'show_user', name="show_user"),
    url(r'^(?P<user_id>\d+)/planuj/urlop/$', 'plan_days', name="plan_days"),
    url(r'^(?P<user_id>\d+)/zglos/obecnosc/$', 'present', name="present"),
    url(r'^(?P<user_id>\d+)/zglos/obecnosc/w/dniu/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'single_present', name='single_present'),
    url(r'^(?P<user_id>\d+)/zglos/chorobe/w/okresie/$', 'sick', name='sick'),
    url(r'^pokaz/obecnosc/w/dniu/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'show_present', name='show_present'),
)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)



