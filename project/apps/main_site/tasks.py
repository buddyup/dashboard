import datetime
import requests

from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from celery.task import task, periodic_task

from main_site.models import DataPoint, DataPointAggregate, Milestone, DASHBOARD_DATA_KEY


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

# curl https://api.intercom.io/segments -u 5714bb0i:a759c4939f3a832e88e0f9cb5c29ffecf6b032c8 -H 'Accept:application/json'
SEGMENT_MAPPING_BY_ID = {
    "544fddd77cdcd41924000003": "num_with_one_class",
    "544fde65ad77a64760000001": "num_attended_one_event",
    "544fe5c809b3d12668000016": "num_total_users",
    "544fe5f43cb3387432000001": "num_filled_in_profile",
    "544fde2b644dee2065000006": "num_with_one_buddy",
    "544fdc67e1e6e662f8000037": "num_hit_home_page",
    "544fdcbef34e7b4f36000072": "num_authenticated",
    "545b9e6114d10246560000df": "num_active_users",
}


@task(name="get_data")
def get_data():
    data = {}

    # Get the big counts, etc.
    headers = {'content-type': 'application/json', 'accept': 'application/json'}

    data["recorded_at"] = datetime.datetime.now()
    print "Recording at %s" % data["recorded_at"]

    # Get the ratio.

    # Loop through all the ACTIVE (last 6 mo) users, get total
    num_buddy_requests = 0
    num_buddies = 0
    per_page = 50

    for key, name in SEGMENT_MAPPING_BY_ID.items():
        end = False
        num_users = 0
        page = 0
        print name
        url = "https://api.intercom.io/users?segment_id=%s&per_page=%s&page=%s" % (key, per_page, page)
        r = requests.get(url, data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
        resp = r.json()
        num_users = resp["total_count"]
        # while not end:
        #     print page

            # url = "https://api.intercom.io/users?segment_id=%s&per_page=%s&page=%s" % (key, per_page, page)
            # r = requests.get(url, data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
            # resp = r.json()
            # num_users = 
            # print resp
            # if "pages" in resp and "next" in resp["pages"] and resp["pages"]["next"]:
            #     url = resp["pages"]["next"]
            #     num_users += per_page
            #     page += 1
            # else:
            #     for u in r.json()["users"]:
            #         num_users += 1
            #     end = True

        data[name] = num_users

    end = False
    page = 0
    num_users = 0
    segment_id = "545b9e6114d10246560000df"
    url = "https://api.intercom.io/users?segment_id=%s&per_page=50&page=%s" % (segment_id, page)


    r = requests.get(url, data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
    resp = r.json()
    num_users = resp["total_count"]
    while page * per_page < num_users:
        url = "https://api.intercom.io/users?segment_id=%s&per_page=50&page=%s" % (segment_id, page)
        r = requests.get(url, data=None, headers=headers, auth=('5714bb0i', settings.INTERCOM_API_KEY))
        users = r.json()["users"]
        for u in users:
            # Ignore weird 
            if "num_buddies" in u["custom_attributes"]:
                num_buddies += int(u["custom_attributes"]["num_buddies"])
                # TODO: Fix this when we keep it more sanely
                num_buddy_requests += int(u["custom_attributes"]["num_buddies"]) + int(u["custom_attributes"]["num_sent_requests"])
            else:
                print "Ignoring %s" % (u["email"])

        page = page + 1

    data["num_buddy_requests"] = num_buddy_requests
    data["num_buddies"] = num_buddies
    data["buddy_ratio"] = float(num_buddies) / float(num_buddy_requests)

    d = DataPoint.objects.create(**data)
    update_aggregates()
    update_dashboard_cache()

def update_aggregates():
    DataPointAggregate.objects.all().delete()

    num_points = 0
    last_day = -1
    for d in DataPoint.objects.order_by("recorded_at").all():
        print d.recorded_at.day
        if d.recorded_at.day != last_day:
            if num_points > 0:
                DataPointAggregate.objects.create(**{
                    "recorded_at": last_point.recorded_at,
                    "num_total_users": num_total_users / num_points,
                    "num_active_users": num_active_users / num_points,
                    "num_authenticated": num_authenticated / num_points,
                    "num_filled_in_profile": num_filled_in_profile / num_points,
                    "num_hit_home_page": num_hit_home_page / num_points,
                    "num_with_one_class": num_with_one_class / num_points,
                    "num_with_one_buddy": num_with_one_buddy / num_points,
                    "num_attended_one_event": num_attended_one_event / num_points,
                    "num_buddy_requests": num_buddy_requests / num_points,
                    "num_buddies": num_buddies / num_points,
                })
                last_day = last_point.recorded_at.day

            num_total_users = 0
            num_active_users = 0
            num_authenticated = 0
            num_filled_in_profile = 0
            num_hit_home_page = 0
            num_with_one_class = 0
            num_with_one_buddy = 0
            num_attended_one_event = 0
            num_buddy_requests = 0
            num_buddies = 0
            num_points = 0

        num_total_users += d.num_total_users
        num_active_users += d.num_active_users
        num_authenticated += d.num_authenticated
        num_filled_in_profile += d.num_filled_in_profile
        num_hit_home_page += d.num_hit_home_page
        num_with_one_class += d.num_with_one_class
        num_with_one_buddy += d.num_with_one_buddy
        num_attended_one_event += d.num_attended_one_event
        num_buddy_requests += d.num_buddy_requests
        num_buddies += d.num_buddies
        last_point = d
        num_points += 1



@task(name="update_dashboard_cache")
def update_dashboard_cache():
    data_points = DataPointAggregate.objects.all()
    milestones = Milestone.objects.all()
    cache.set(DASHBOARD_DATA_KEY, render_to_string("main_site/dashboard_data.js", locals()))

