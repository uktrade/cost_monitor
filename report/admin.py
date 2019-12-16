from django.contrib import admin
from report.models import ReportDate

# Register your models here.
@admin.register(ReportDate)
class ReportDatesAdmin(admin.ModelAdmin):
    list_display = ('month', 'start_date', 'end_date')
