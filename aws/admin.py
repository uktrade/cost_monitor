from django.contrib import admin
from aws.models import AwsReportDates,AwsAccounts,AwsAccountCost
# Register your models here.


@admin.register(AwsReportDates)
class AwsReportDatesAdmin(admin.ModelAdmin):
    list_display = ('month', 'start_date', 'end_date')

@admin.register(AwsAccounts)
class AwsAccountsAdmin(admin.ModelAdmin):
    list_display = ('report_date','id','name')
@admin.register(AwsAccountCost)
class AwsAccountCostAdmin(admin.ModelAdmin):
    list_display = ('account','amount')
