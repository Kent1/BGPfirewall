from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^neighbor/', include('neighbor.urls')),
    url(r'^flow/', include('flow.urls')),
    # Examples:
    # url(r'^$', 'BGPfirewall.views.home', name='home'),
    # url(r'^BGPfirewall/', include('BGPfirewall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
