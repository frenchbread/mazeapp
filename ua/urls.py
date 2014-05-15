from django.conf.urls import patterns, include, url
from views import profile, follow, unfollow, profilelikes, profileinfo, profilefollowing, profilefollowers

urlpatterns = patterns('',
    url(r'^(?P<username>\w+)/$', profile, name="profile"),
    url(r'^(?P<username>\w+)/likes', profilelikes, name="profilelikes"),
    url(r'^(?P<username>\w+)/info', profileinfo, name="profileinfo"),
    url(r'^(?P<username>\w+)/following', profilefollowing, name="profilefollowing"),
    url(r'^(?P<username>\w+)/followers', profilefollowers, name="profilefollowers"),
    url(r'^follow/(?P<target_id>\w+)/$', follow, name="follow"),
    url(r'^unfollow/(?P<target_id>\w+)/$', unfollow, name="unfollow"),
)
