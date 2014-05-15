from django.conf.urls import patterns, include, url
from mm.views import amap

urlpatterns = patterns('',
    url(r'^map/$', amap , name='map'),
)