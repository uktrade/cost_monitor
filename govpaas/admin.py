from django.contrib import admin

from .models import BillingData, Space


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("team", "space")


@admin.register(BillingData)
class BilllingDataAdmin(admin.ModelAdmin):
    list_display = ("org", "space", "year", "month", "complete", "amount", "forecast", "percentage_change")
    list_filter = ("org", "space", "year", "month", "complete")
