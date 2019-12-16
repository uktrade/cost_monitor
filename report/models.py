from django.db import models

# Create your models here.

class ReportDate(models.Model):
    month = models.IntegerField(primary_key=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)