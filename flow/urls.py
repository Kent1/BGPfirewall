"""
Url manager

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.conf.urls import patterns, url

from flow import views

urlpatterns = patterns('',
    # ex: /flow/
    url(r'^$', views.ListView.as_view(), name='flow_list'),
    # ex: /flow/1/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='flow_detail'),
    # ex: /flow/create/
    url(r'^add/$', views.CreateView.as_view(), name='flow_add')
)
