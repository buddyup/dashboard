import datetime
import json
from django.db import models
from django.conf import settings


MILESTONE_TYPES = [("code_push", "Code Push"), ("event", "Event")]


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DataPoint(BaseModel):
    recorded_at = models.DateTimeField(default=datetime.datetime.now())

    num_total_users = models.IntegerField(verbose_name='Total')
    num_active_users = models.IntegerField(verbose_name='Active')
    num_authenticated = models.IntegerField(verbose_name='Authenticated')
    num_filled_in_profile = models.IntegerField(verbose_name='Filled in profile')
    num_hit_home_page = models.IntegerField(verbose_name='Hit home page')
    num_with_one_class = models.IntegerField(verbose_name='1+ Class')
    num_with_one_buddy = models.IntegerField(verbose_name='1+ Buddy')
    num_attended_one_event = models.IntegerField(verbose_name='Attended an event')
    num_buddy_requests = models.IntegerField(verbose_name='Buddy Requests')
    num_buddies = models.IntegerField(verbose_name='Buddies')
    buddy_ratio = models.FloatField()

    def __unicode__(self):
        return "%s" % self.recorded_at

    @property
    def json(self):
        return json.dumps({
            "uid": "data_%s" % self.id,
            "recorded_at": int(self.recorded_at.strftime("%s")),
            "display_date": self.recorded_at.strftime("%B %d %Y %I %p"),
            "num_total_users": self.num_total_users,
            "num_active_users": self.num_active_users,
            "num_authenticated": self.num_authenticated,
            "num_filled_in_profile": self.num_filled_in_profile,
            "num_hit_home_page": self.num_hit_home_page,
            "num_with_one_class": self.num_with_one_class,
            "num_with_one_buddy": self.num_with_one_buddy,
            "num_attended_one_event": self.num_attended_one_event,
            "num_buddy_requests": self.num_buddy_requests,
            "num_buddies": self.num_buddies,
            "buddy_ratio": self.buddy_ratio,
            "type": "data_point",
        })

class Milestone(BaseModel):
    name = models.CharField(max_length=200)
    recorded_at = models.DateTimeField(default=datetime.datetime.now())
    type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    before_pic_1 = models.ImageField(upload_to="before_after", blank=True, null=True)
    before_pic_2 = models.ImageField(upload_to="before_after", blank=True, null=True)
    before_pic_3 = models.ImageField(upload_to="before_after", blank=True, null=True)
    after_pic_1 = models.ImageField(upload_to="before_after", blank=True, null=True)
    after_pic_2 = models.ImageField(upload_to="before_after", blank=True, null=True)
    after_pic_3 = models.ImageField(upload_to="before_after", blank=True, null=True)
    
    def json_picture_url(self, pic):
        if pic:
            return "%s" % pic.url
        else:
            return ""

    class Meta:
        ordering = ("recorded_at",)

    def __unicode__(self):
        return "%s" % self.name

    @property
    def json(self):
        return json.dumps({
            "uid": "milestone_%s" % self.id,
            "name": self.name,
            "recorded_at": int(self.recorded_at.strftime("%s")),
            "display_date": self.recorded_at.strftime("%B %d %Y, %I %p"),
            "type": self.type,
            "before_pic_1": self.json_picture_url(self.before_pic_1),
            "before_pic_2": self.json_picture_url(self.before_pic_2),
            "before_pic_3": self.json_picture_url(self.before_pic_3),
            "after_pic_1": self.json_picture_url(self.after_pic_1),
            "after_pic_2": self.json_picture_url(self.after_pic_2),
            "after_pic_3": self.json_picture_url(self.after_pic_3),
        })
