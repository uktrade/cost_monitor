from django.db import models

# Create your models here.


class AwsReportDates(models.Model):
    month = models.IntegerField(primary_key=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Aws Report Dates"
class AwsAccounts(models.Model):
    pk_id = models.AutoField(primary_key=True)
    report_date = models.ForeignKey('AwsReportDates',on_delete=models.CASCADE)
    id = models.IntegerField()
    name = models.CharField(max_length=100)
   
    class Meta:
        verbose_name_plural = "Aws Accounts"
class AwsAccountCost(models.Model):
    pk_id = models.AutoField(primary_key=True)
    account = models.ForeignKey('AwsAccounts',on_delete=models.CASCADE)
    amount = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Aws Account Cost"
