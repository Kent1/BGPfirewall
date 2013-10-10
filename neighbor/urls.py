"""
Url manager

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.conf.urls import patterns, url

from neighbor import views

urlpatterns = patterns('',
    # ex: /neighbor/
    url(r'^$', views.ListView.as_view(), name='index'),
    # ex: /neighbor/1/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /neighbor/create/
    url(r'^create/$', views.CreateView.as_view(), name='create')
)
