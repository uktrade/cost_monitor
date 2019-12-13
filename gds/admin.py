from django.contrib import admin
from gds.models import GDSOrganization, GDSOrganizationsSpace, GDSCost

# Register your models here.
@admin.register(GDSOrganization)
class GDSOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(GDSOrganizationsSpace)
class GDSOrganizationsSpaceAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'id', 'name')


@admin.register(GDSCost)
class GDSCostAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'organization_id', 'space_id', 'amount')
