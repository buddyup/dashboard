from annoying.decorators import render_to
from main_site.models import DataPoint, Milestone

@render_to("main_site/home.html")
def home(request):
    data_points = DataPoint.objects.all()
    milestones = Milestone.objects.all()
    
    return locals()
