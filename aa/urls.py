from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required as auth
from views import allposts, newpost, like, unlike, post, deletepost, editpost, allpeople

urlpatterns = patterns('',
                url(r'^all/$', allposts,  name='allposts'),
                url(r'^people/$', allpeople,  name='allpeople'),
                url(r'^newpost/$', newpost,  name='newpost'),
                url(r'^like/(?P<target_id>\w+)/$', like, name="like"),
                url(r'^unlike/(?P<target_id>\w+)/$', unlike, name="like"),
                url(r'^p/(?P<post_id>\w+)/$', post, name='post'),
                url(r'^p/delete/(?P<post_id>\w+)/$', deletepost, name='deletepost'),
                url(r'^p/edit/(?P<post_id>\d+)/$', editpost, name='editpost'),
                #url(r'^delete/(?P<pk>\d+)/$', auth(ClipDelete.as_view()), name='deletepost'),
                #url(r'^like/$', auth(LikeViewTwo.as_view()), name="like"),
                )

