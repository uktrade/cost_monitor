from django.db import models
from report.models import ReportDate

# Create your models here.
class HerokuTeam(models.Model):
    pk_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class HerokuCost(models.Model):
    pk_id = models.AutoField(primary_key=True)
    report_date = models.ForeignKey('report.ReportDate',on_delete=models.CASCADE)
    team = models.ForeignKey('HerokuTeam',on_delete=models.CASCADE)
    amount = models.FloatField()

class HerokuForecast(models.Model):
    pk_id = models.AutoField(primary_key=True)
    cost_id = models.ForeignKey('HerokuCost',on_delete=models.CASCADE)
    amount = models.FloatField()
    difference = models.FloatField()