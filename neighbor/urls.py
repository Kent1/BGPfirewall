from django.conf.urls import patterns, url

from neighbor import views

urlpatterns = patterns('',
    # ex: /neighbor/
    url(r'^$', views.index, name='index'),
    # ex: /neighbor/1/
    url(r'^(?P<neighbor_id>\d+)/$', views.detail, name='detail')
)
