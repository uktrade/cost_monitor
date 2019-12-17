from prometheus_client import Gauge
from aws.helper.manager import AwsRecordManager
from gds.helper.manager import GDSRecordManager
from heroku.helper.manager import HerokuRecordManager


class Prometheus:
    
    def exportAws(self):
        awsCostMetric = Gauge('dit_aws_cost_monitor','AWSCostMonitor for Dit',['startDate','endDate','account','amount','month'])

        costData = AwsRecordManager().getCost()

        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            account = cost.account.name
            amount = cost.amount

            awsCostMetric.labels(startDate,endDate,account,amount,month)
     
    def exportGDS(self):
        gdsCostMetric = Gauge('dit_gds_cost_monitor','GDSCostMonitor for Dit',['startDate','endDate','organization','space','amount','month'])

        costData = GDSRecordManager().getCost()
        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            organization = cost.organization_id.name
            space = cost.space_id.name
            amount = cost.amount
            gdsCostMetric.labels(startDate,endDate,organization,space,amount,month)

    def exportHeroku(self):
        herokuCostMetric = Gauge('dit_heroku_cost_monitor','HerokuCostMonitor for Dit',['startDate','endDate','account','amount','month'])
        costData = HerokuRecordManager().getCoast()
        for cost in costData:
            month = cost.report_date.month
            startDate = cost.report_date.start_date
            endDate = cost.report_date.end_date
            account = cost.team.name
            amount = cost.amount
            herokuCostMetric.labels(startDate,endDate,account,amount,month)



class PrometheusForecast:

    def exportAwsForecast(self):
        awsForecastMetric = Gauge('dit_aws_cost_forecast','AWSCostForecast for Dit',['startDate','account','amount','difference_in_percentage'])

        costData = AwsRecordManager().getForecast()
        breakpoint()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.account.name
            amount = cost.amount
            difference = cost.difference
            awsForecastMetric.labels(startDate,account,amount,difference)
     
    def exportGDSForecast(self):
        gdsForecastMetric = Gauge('dit_gds_cost_forecast','GDSCostForecast for Dit',['startDate','organization','space','amount','difference_in_percentage'])

        costData = GDSRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            organization = cost.cost_id.organization_id.name
            space = cost.cost_id.space_id.name
            amount = cost.amount
            difference = cost.difference
            gdsForecastMetric.labels(startDate,organization,space,amount,difference)

    def exportHerokuForecast(self):
        herokuForecastMetric = Gauge('dit_heroku_cost_forecast','HerokuCostForecast for Dit',['startDate','endDate','account','amount','month','difference_in_percentage'])
        costData = HerokuRecordManager().getForecast()
        for cost in costData:
            startDate = cost.cost_id.report_date.start_date
            account = cost.cost_id.team.name
            amount = cost.amount
            difference = cost.difference
            herokuForecastMetric.labels(startDate,account,amount,difference)
