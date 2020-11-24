from django.contrib import admin
from aws.models import AwsAccount, AwsAccountCost, AwsForecast, AwsTeamAccountAssociation
# Register your models here.


@admin.register(AwsAccount)
class AwsAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(AwsTeamAccountAssociation)
class AwsTeamAccountAssociationAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'team')


@admin.register(AwsAccountCost)
class AwsAccountCostAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'account', 'amount')


@admin.register(AwsForecast)
class AwsForecastAdmin(admin.ModelAdmin):
    list_display = ('cost_id', 'amount', 'difference')
