from django.conf.urls import patterns, include, url
from aa.views import home
from ua.views import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required as auth
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home , name='home'),
    url(r'^settings/$', auth(settings) , name='settings'),
    url(r'^u/', include('ua.urls')),
    url(r'^m/', include('mm.urls')),
    url(r'^a/', include('aa.urls')),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)