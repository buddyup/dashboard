from django.contrib import admin
from main_site.models import DataPoint, Milestone


class DataPointAdmin(admin.ModelAdmin):
    list_display = ("recorded_at", "num_total_users", "num_authenticated", 
                    "num_filled_in_profile", "num_hit_home_page", "num_with_one_class", 
                    "num_with_one_buddy", "num_attended_one_event", )
    model = DataPoint


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("name", "recorded_at", "type")
    model = Milestone

admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(DataPoint, DataPointAdmin)
