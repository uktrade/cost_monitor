from django.contrib import admin
from aws.models import AwsAccount,AwsAccountCost,AwsForecast
# Register your models here.

@admin.register(AwsAccount)
class AwsAccountAdmin(admin.ModelAdmin):
    list_display = ('id','name')
@admin.register(AwsAccountCost)
class AwsAccountCostAdmin(admin.ModelAdmin):
    list_display = ('report_date','account','amount')

@admin.register(AwsForecast)
class AwsForecastAdmin(admin.ModelAdmin):
    list_display = ('account','amount','difference')