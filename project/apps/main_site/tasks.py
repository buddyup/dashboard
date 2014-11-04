from celery.task import task, periodic_task
import datetime
import requests
from django.conf import settings
from main_site.models import DataPoint


SEGMENT_MAPPING = {
    "Added One Course": "num_with_one_class",
    "Attended One Event": "num_attended_one_event",
    "Everyone": "num_total_users",
    "Filled In Profile": "num_filled_in_profile",
    "Has One Buddy": "num_with_one_buddy",
    "Hit Home Page": "num_hit_home_page",
    "Logged In": "num_authenticated",
}


@task(name="get_data")
def get_data():
    headers = {'content-type': 'application/json', 'accept': 'application/json'}

    r = requests.get('https://api.intercom.io/counts?type=user&count=segment', data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
    segments = r.json()["user"]["segment"]

    data = {}
    for s in segments:
        for name, value in s.items():
            if name in SEGMENT_MAPPING:
                data[SEGMENT_MAPPING[name]] = value

    data["recorded_at"] = datetime.datetime.now()

    d = DataPoint.objects.create(**data)