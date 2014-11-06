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
    "Active after Intercom was added": "num_active_users",

}


@task(name="get_data")
def get_data():

    # Get the big counts, etc.
    headers = {'content-type': 'application/json', 'accept': 'application/json'}

    r = requests.get('https://api.intercom.io/counts?type=user&count=segment', data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
    segments = r.json()["user"]["segment"]
    data = {}
    for s in segments:
        for name, value in s.items():
            if name in SEGMENT_MAPPING:
                data[SEGMENT_MAPPING[name]] = value

    data["recorded_at"] = datetime.datetime.now()
    print "Recording at %s" % data["recorded_at"]

    # Get the ratio.

    # Loop through all the ACTIVE (last 6 mo) users, get totay
    page = 0
    segment_id = "545b9e6114d10246560000df"
    url = "https://api.intercom.io/users?segment_id=%s&per_page=50&page=%s" % (segment_id, page)

    end = False
    num_users = 0
    num_buddy_requests = 0
    num_buddies = 0

    while not end:
        r = requests.get(url, data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
        resp = r.json()

        users = r.json()["users"]
        for u in users:
            # Ignore weird 
            if "num_buddies" in u["custom_attributes"]:
                num_users += 1
                num_buddies += int(u["custom_attributes"]["num_buddies"])
                # TODO: Fix this when we keep it more sanely
                num_buddy_requests += int(u["custom_attributes"]["num_buddies"]) + int(u["custom_attributes"]["num_sent_requests"])
            else:
                print "Ignoring %s" % (u["email"])

        if "next" in resp["pages"] and resp["pages"]["next"]:
            url = resp["pages"]["next"]
        else:
            end = True

    data["num_buddy_requests"] = num_buddy_requests
    data["num_buddies"] = num_buddies
    data["buddy_ratio"] = float(num_buddies) / float(num_buddy_requests)

    d = DataPoint.objects.create(**data)

