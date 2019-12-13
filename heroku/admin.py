from django.contrib import admin
from heroku.models import HerokuTeam,HerokuCost

# Register your models here.
@admin.register(HerokuTeam)
class HerokuTeamAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(HerokuCost)
class HerokuCostAdmin(admin.ModelAdmin):
    list_display = ('report_date','team','amount')