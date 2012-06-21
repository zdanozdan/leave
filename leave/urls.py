from django.conf.urls import patterns, include, url

urlpatterns = patterns('leave.views',
    url(r'^$', 'index'),
    url(r'^show/(?P<user_id>\d+)/user/$', 'show_user', name="show_user"),
    url(r'^plan/(?P<user_id>\d+)/user/$', 'plan_days', name="plan_days"),
    url(r'^planned/(?P<user_id>\d+)/user/$', 'planned_days', name="planned_days"),
)



