from django.contrib import admin
from heroku.models import HerokuTeam, HerokuCost, HerokuForecast

# Register your models here.
@admin.register(HerokuTeam)
class HerokuTeamAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(HerokuCost)
class HerokuCostAdmin(admin.ModelAdmin):
    list_display = ('report_date','team','amount')


@admin.register(HerokuForecast)
class HerokuForecastAdmin(admin.ModelAdmin):
    list_display = ('cost_id','amount','difference')