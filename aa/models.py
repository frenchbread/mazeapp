from django.db import models
from time import time
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from ua.models import Member


def get_upload_place(instance, filename):
    return "uploaded_files/posts/%s/%s" % (instance.user, str(time()).replace('.', '_')+filename)


class LikeCount(models.Manager):
    def get_query_set(self):
        return super(LikeCount, self).get_query_set().annotate(likes=Count('like')).order_by('-timestamp')


class Post(models.Model):
    user = models.ForeignKey(Member)
    title = models.CharField("Headline", max_length=100)
    body = models.TextField(max_length=1000)
    rank_score = models.FloatField(default=0.0)
    pic = models.FileField(upload_to=get_upload_place, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    with_likes = LikeCount()
    objects = models.Manager()  # default

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": str(self.id)})

    def set_rank(self):
        sec_in_h = float(5)
        gravity = 1.2

        delta = now() - self.timestamp
        item_hour_age = delta.total_seconds() // sec_in_h
        likes = self.likes - 1
        self.rank_score = likes / pow((item_hour_age+2), gravity)
        self.save()


class Like(models.Model):
    user = models.ForeignKey(Member)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "%s liked %s" % (self.user.username, self.post.title)