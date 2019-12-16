from django.db import models

# Create your models here.

class AwsAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
   
class AwsAccountCost(models.Model):
    pk_id = models.AutoField(primary_key=True)
    report_date = models.ForeignKey('report.ReportDate',on_delete=models.CASCADE)
    account = models.ForeignKey('AwsAccount',on_delete=models.CASCADE)
    amount = models.FloatField(null=True)

class AwsForecast(models.Model):
    id = models.AutoField(primary_key=True)
    account= models.ForeignKey('AwsAccount',on_delete=models.CASCADE)
    amount = models.FloatField()
    difference = models.FloatField()