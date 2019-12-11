from django.db import models

# Create your models here.

class HerokuReportDate(models.Model):
    month = models.IntegerField(primary_key=True)
    start_date = models.DateField(auto_now=False,auto_now_add=False)
class HerokuTeam(models.Model):
    pk_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class HerokuCost(models.Model):
    pk_id = models.AutoField(primary_key=True)
    report_date = models.ForeignKey('HerokuReportDate',on_delete=models.CASCADE)
    team = models.ForeignKey('HerokuTeam',on_delete=models.CASCADE)
    amount = models.IntegerField()
