import datetime as dt
import os

from prometheus_client import CollectorRegistry, Gauge

from aws.helper.manager import AwsRecordManager
from govpaas.models import BillingData, lookup_team_name


class PrometheusForecast:

    def __init__(self, registry):
        self.registry = registry
        self.awsForecastMetric = Gauge('aws_cost_forecast', 'AWSCostForecast for Dit', [
                                        'account', 'team'], registry=self.registry)
        self.gdsForecastMetric = Gauge('gds_cost_forecast', 'GDSCostForecast for Dit', [
                                        'organization', 'space', 'team'], registry=self.registry)

    def exportAwsForecast(self):

        costData = AwsRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.account.name
            team = AwsRecordManager().getAssociatedTeamByAccountName(
                account_name=account)[0].team
            self.awsForecastMetric.labels(account,team).set(cost.amount)

    def exportGDSForecast(self):
        today = dt.date.today()

        billing_data = BillingData.objects.exclude(space="").filter(year=today.year, month=today.month)

        for item in billing_data:
            team = lookup_team_name(item.space)
            self.gdsForecastMetric.labels(item.org, item.space, team).set(item.amount)
