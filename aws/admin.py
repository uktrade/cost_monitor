from django.contrib import admin
from aws.models import AwsReportDates, AwsAccounts, AccountsCost
# Register your models here.


@admin.register(AwsReportDates)
class AwsReportDatesAdmin(admin.ModelAdmin):
    list_display = ('month', 'start_date', 'end_date')


@admin.register(AwsAccounts)
class AwsAccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(AccountsCost)
class AccountsCostAdmin(admin.ModelAdmin):
    list_display = ('month', 'account_id', 'amount')
