from django.db import models

# Create your models here.


class AwsReportDates(models.Model):
    month = models.IntegerField(primary_key=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Aws Report Dates"


class AwsAccounts(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Aws Accounts"


class AccountsCost(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.ForeignKey('AwsReportDates', on_delete=models.CASCADE)
    account_id = models.ForeignKey('AwsAccounts', on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        verbose_name_plural = "Aws Cost"
