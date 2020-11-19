from report.helper.reportDates import ReportDates
from report.helper.reportMonths import ReportMonths
from report.helper.manager import ReportManager
from report.helper.gecko import cleint as gecko_client

from aws.collector import Collector as awsCollector
from gds.collector import Collector as GDSCollector


from aws.forecast import Forecast as awsForecast
from gds.forecast import Forecast as gdsForecast

from prometheus_client import Gauge,CollectorRegistry
from aws.helper.manager import AwsRecordManager
from gds.helper.manager import GDSRecordManager

from operator import itemgetter
import requests
from django.conf import settings
class Processor:

    def __init__(self):
        self.reportDates = ReportDates()
        self.reportManager = ReportManager()

    def setReportDates(self):
        for month in ReportMonths:
            month, start_date, end_date = ReportDates(
            ).startAndendDateForMonth(month=month.value)
            self.reportManager.updateReportDate(
                month=month, start_date=start_date, end_date=end_date)

    def __awsCollector(self):
        report_dates = self.reportManager.reportDates()
        linked_accounts_start_date = self.reportManager.reportDatesByMonth(
            ReportMonths.CURRENT_MONTH_MINUS_6.value)[0].start_date
        linked_accounts_end_date = self.reportManager.reportDatesByMonth(
            ReportMonths.CURRENT_MONTH.value)[0].end_date

        awsCollector().run(report_dates=report_dates, linked_accounts_start_date=linked_accounts_start_date,
                           linked_accounts_end_date=linked_accounts_end_date)

    def __gdsCollector(self):
        report_dates = self.reportManager.reportDates()
        GDSCollector().run(report_dates=report_dates)

    def runCollectors(self):
        self.__awsCollector()
        self.__gdsCollector()

    def runForecasters(self):
        awsForecast()
        gdsForecast()


    def exportMetrics(self):
        webClient = requests.session()
        from config.urls import urlpatterns
        requests.get(f'http://localhost:{settings.PORT}/export/forecast')        

    def exportAwsForecastToGeckoboard(self,widget_uuid):
        forecast_data = list()
        costData = AwsRecordManager().getForecast()

        for cost in costData:
            forecast_data.append({'name': cost.cost_id.account.name, 'forecast': float(
                    format(cost.amount, '.2f')), 'percent_diff': float(format(cost.difference, '.2f'))})

        payload = gecko_client().leaderboard_format(data=sorted(forecast_data, key=itemgetter('forecast'), reverse=True))

        gecko_client().push(widget_uuid=widget_uuid,payload=payload)


    def exportGDSForecastToGeckoboard(self,widget_uuid):
        forecast_data = list()
        costData = GDSRecordManager().getForecast()

        for cost in costData:
            forecast_data.append({'name': f'{cost.cost_id.organization_id.name}/{cost.cost_id.space_id.name}', 'forecast': float(
                    format(cost.amount, '.2f')), 'percent_diff': float(format(cost.difference, '.2f'))})

        payload = gecko_client().leaderboard_format(data=sorted(forecast_data, key=itemgetter('forecast'), reverse=True))

        gecko_client().push(widget_uuid=widget_uuid,payload=payload)
