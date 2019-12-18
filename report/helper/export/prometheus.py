from prometheus_client import Gauge
from aws.helper.manager import AwsRecordManager
from gds.helper.manager import GDSRecordManager
from heroku.helper.manager import HerokuRecordManager

class Prometheus:

    def __init__(self):
        self.awsCostMetric = Gauge('dit_aws_cost_monitor','AWSCostMonitor for Dit',['startDate','endDate','account','amount','month'])
        self.gdsCostMetric = Gauge('dit_gds_cost_monitor','GDSCostMonitor for Dit',['startDate','endDate','organization','space','amount','month'])
        self.herokuCostMetric = Gauge('dit_heroku_cost_monitor','HerokuCostMonitor for Dit',['startDate','endDate','account','amount','month'])

    def exportAwsCost(self):
        
        costData = AwsRecordManager().getCost()
        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            account = cost.account.name
            amount = cost.amount
            self.awsCostMetric.labels(startDate,endDate,account,amount,month)
     
    def exportGDSCost(self):
        
        costData = GDSRecordManager().getCost()
        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            organization = cost.organization_id.name
            space = cost.space_id.name
            amount = cost.amount
            self.gdsCostMetric.labels(startDate,endDate,organization,space,amount,month)

    def exportHerokuCost(self):

        costData = HerokuRecordManager().getCoast()
        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            account = cost.team.name
            amount = cost.amount
            self.herokuCostMetric.labels(startDate,endDate,account,amount,month)

class PrometheusForecast:

    def __init__(self):
        self.awsForecastMetric = Gauge('dit_aws_cost_forecast','AWSCostForecast for Dit',['startDate','account','amount','difference_in_percentage'])
        self.gdsForecastMetric = Gauge('dit_gds_cost_forecast','GDSCostForecast for Dit',['startDate','organization','space','amount','difference_in_percentage'])
        self.herokuForecastMetric = Gauge('dit_heroku_cost_forecast','HerokuCostForecast for Dit',['startDate','account','amount','difference_in_percentage'])


    def exportAwsForecast(self):
        
        costData = AwsRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.account.name
            amount = cost.amount
            difference = cost.difference
            self.awsForecastMetric.labels(startDate,account,amount,difference)
     
    def exportGDSForecast(self):
        
        costData = GDSRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            organization = cost.cost_id.organization_id.name
            space = cost.cost_id.space_id.name
            amount = cost.amount
            difference = cost.difference
            self.gdsForecastMetric.labels(startDate,organization,space,amount,difference)

    def exportHerokuForecast(self):

        costData = HerokuRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.team.name
            amount = cost.amount
            difference = cost.difference
            self.herokuForecastMetric.labels(startDate,account,amount,difference)
