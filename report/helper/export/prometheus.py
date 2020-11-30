from prometheus_client import Gauge,CollectorRegistry
from aws.helper.manager import AwsRecordManager
from gds.helper.manager import GDSRecordManager
 
from prometheus_client import CollectorRegistry, Gauge
import os
class PrometheusForecast:

    def __init__(self):    
        self.registry = CollectorRegistry()
        self.awsForecastMetric = Gauge('aws_cost_forecast', 'AWSCostForecast for Dit', [
                                       'startDate', 'account', 'team'],registry=self.registry)
        self.gdsForecastMetric = Gauge('gds_cost_forecast', 'GDSCostForecast for Dit', [
                                       'startDate', 'organization', 'space', 'team'],registry=self.registry)
        self.awsExpectedChangeMetric = Gauge('aws_estimated_change_forecast', 'An estimate of (signed) Diffrence in Bill from Previous Month', [
                                       'startDate', 'account', 'team'],registry=self.registry)
        self.gdsExpectedChangetMetric = Gauge('gds_estimated_change_forecast', 'An estimate of (signed) Diffrence in Bill from Previous Month', [
                                       'startDate', 'organization', 'space', 'team'],registry=self.registry)

    def getRegistry(self):
        return self.registry
    
    def exportAwsForecast(self):

        costData = AwsRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.account.name
            team = AwsRecordManager().getAssociatedTeamByAccountName(
                account_name=account)[0].team
            self.awsForecastMetric.labels(startDate,account,team).set(cost.amount)
            self.awsExpectedChangeMetric.labels(startDate,account,team).set(cost.difference)


    def exportGDSForecast(self):
    
        costData = GDSRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            organization = cost.cost_id.organization_id.name
            space = cost.cost_id.space_id.name
            team = GDSRecordManager().getAssociatedTeamNameBySpaceName(
                space_name=space)[0].team
            self.gdsForecastMetric.labels(
                startDate, organization, space, team).set(cost.amount)
            self.gdsExpectedChangetMetric.labels(
                startDate, organization, space, team).set(cost.difference)
