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

