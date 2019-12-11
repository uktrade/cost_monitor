from django.contrib import admin
from heroku.models import HerokuReportDate,HerokuTeam,HerokuCost
# Register your models here.

@admin.register(HerokuReportDate)
class HerokuReportDateAdmin(admin.ModelAdmin):
    list_display = ('month','start_date')


@admin.register(HerokuTeam)
class HerokuTeamAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(HerokuCost)
class HerokuCostAdmin(admin.ModelAdmin):
    list_display = ('report_date','team','amount')