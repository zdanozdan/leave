from django.conf.urls import patterns, include, url

urlpatterns = patterns('leave.views',
    url(r'^$', 'index'),
#    url(r'^(?P<poll_id>\d+)/$', 'index'),
#    url(r'^(?P<poll_id>\d+)/results/$', 'results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)



