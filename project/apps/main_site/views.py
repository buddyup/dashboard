import json

from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from main_site.models import DataPoint, Milestone, Sale


@login_required
@render_to("main_site/home.html")
def home(request):
    data_points = DataPoint.objects.all()
    milestones = Milestone.objects.all()
    
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
            s.status = sale["value"]
            s.save()
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