import json
import requests

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from annoying.decorators import render_to, ajax_request
from main_site.models import DataPoint, Milestone, Sale, DASHBOARD_DATA_KEY
from main_site.tasks import update_dashboard_cache

@login_required
@render_to("main_site/home.html")
def home(request):
    data_points = DataPoint.objects.all()
    milestones = Milestone.objects.all()
    if not cache.get(DASHBOARD_DATA_KEY):
        update_dashboard_cache()

    data_string = cache.get(DASHBOARD_DATA_KEY)
    return locals()


@login_required
@render_to("main_site/sales_cycle.html")
def sales_cycle(request):
    sales = Sale.objects.all()
    
    return locals()

@login_required
@ajax_request
def save_sales(request):
    try:
        data = json.loads(request.body)
        for sale in data:
            s = Sale.objects.get(pk=sale["pk"])
            old_status = "%s" % s.status

            s.status = sale["value"]
            s.save()
            
            if old_status != "%s" % sale["value"]:
                try:
                    s = Sale.objects.get(pk=sale["pk"])
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(
                        "%s/api/sales-update" % settings.WILL_URL, 
                        headers=headers, 
                        data=json.dumps({
                            "name": s.name,
                            "status": s.get_status_display()
                        })
                    )
                    assert r.status_code == 200
                except:
                    import traceback; traceback.print_exc();
                    pass
        return {'success': True}
    except:
        import traceback; traceback.print_exc();
        return {'success': False}


@login_required
@render_to("main_site/intercom.html")
def intercom(request):
    return locals()

@login_required
@render_to("main_site/will.html")
def will(request):
    return locals()

@login_required
@render_to("main_site/admin.html")
def admin(request):
    return locals()