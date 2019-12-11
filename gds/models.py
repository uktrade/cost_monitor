from django.db import models

# Create your models here.


class GDSReportDate(models.Model):
    month = models.IntegerField(primary_key=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)


class GDSOrganization(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)


class GDSOrganizationsSpace(models.Model):
    organization_id = models.ForeignKey(
        'GDSOrganization', on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)


class GDSCost(models.Model):
    pk_id = models.AutoField(primary_key=True)
    report_date = models.ForeignKey('GDSReportDate', on_delete=models.CASCADE)
    organization_id = models.ForeignKey(
        'GDSOrganization', on_delete=models.CASCADE)
    space_id = models.ForeignKey(
        'GDSOrganizationsSpace', on_delete=models.CASCADE)
    amount = models.FloatField()
