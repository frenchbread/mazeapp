from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import hashlib
from time import time
from registration.signals import user_registered


def get_upload_place(instance, filename):
    return "uploaded_files/us_pics/%s/%s" % (instance.user, str(time()).replace('.', '_')+filename)


def gravatar_url(email):
    return "http://www.gravatar.com/avatar/%s?s=100&d=404" % hashlib.md5(email).hexdigest()


class Member(models.Model):
    user = models.OneToOneField(User, unique=True)
    pic = models.FileField(upload_to=get_upload_place, default="default.png", blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.user.username


def create_member_place(sender, instance, **kwargs):
    o, n = Member.objects.get_or_create(user=instance)
    if o:
        print "done"
    else:
        print "not done"

user_registered.connect(create_member_place, sender=User)
User.profile = property(lambda u: Member.objects.get_or_create(user=u)[0])


class FollowUser(models.Model):
    who = models.ForeignKey(Member, related_name="following", unique=False)
    whom = models.ForeignKey(Member, related_name="followers", unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s followed %s" % (self.who.user.username, self.whom.user.username)