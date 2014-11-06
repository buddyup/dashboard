import datetime
from django.db import models


MILESTONE_TYPES = [("code_push", "Code Push"), ("event", "Event")]


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DataPoint(BaseModel):
    recorded_at = models.DateTimeField(default=datetime.datetime.now())

    num_total_users = models.IntegerField()
    num_active_users = models.IntegerField()
    num_authenticated = models.IntegerField()
    num_filled_in_profile = models.IntegerField()
    num_hit_home_page = models.IntegerField()
    num_with_one_class = models.IntegerField()
    num_with_one_buddy = models.IntegerField()
    num_attended_one_event = models.IntegerField()
    num_buddy_requests = models.IntegerField()
    num_buddies = models.IntegerField()
    buddy_ratio = models.FloatField()

    def __unicode__(self):
        return "%s" % self.recorded_at

class Milestone(BaseModel):
    name = models.CharField(max_length=200)
    recorded_at = models.DateTimeField(default=datetime.datetime.now())
    type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    
    class Meta:
        ordering = ("recorded_at",)

    def __unicode__(self):
        return "%s" % self.name
