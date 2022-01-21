import re

from django.db import models


class Space(models.Model):
    team = models.CharField(max_length=255)
    space = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.team} - {self.space}"


class BillingData(models.Model):
    """Monthly per-space billing data."""

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    org = models.CharField(max_length=255)
    space = models.CharField(max_length=255, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    complete = models.BooleanField(default=False, help_text="Do we have a full month's data?")

    forecast = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_change = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["year", "month", "org", "space"], name="unique entry")
        ]
        verbose_name_plural = "billing_data"


def lookup_team_name(space):
    """Look up team name for a given space"""

    if not space:
        return "all spaces"

    try:
        return Space.objects.get(space=space).team
    except Space.DoesNotExist:
        return re.sub(
            '-', '', re.sub('-dev|-staging|-uat|-apps|-demo|-qa|-devpopcorn|-training', '', space))
