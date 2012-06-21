from django.conf.urls import patterns, include, url

urlpatterns = patterns('leave.views',
    url(r'^$', 'index'),
    url(r'^show/(?P<user_id>\d+)/user/$', 'showUser', name="show_user"),
    url(r'^plan/(?P<user_id>\d+)/user/$', 'planDays', name="plan_days"),
    url(r'^planned/(?P<user_id>\d+)/user/$', 'planned_days', name="planned_days"),
)



