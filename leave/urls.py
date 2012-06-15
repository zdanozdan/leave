from django.conf.urls import patterns, include, url

urlpatterns = patterns('leave.views',
    url(r'^$', 'index'),
    url(r'^show/(?P<user_id>\d+)/user/$', 'showUser'),
#    url(r'^(?P<poll_id>\d+)/results/$', 'results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)



