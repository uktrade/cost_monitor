from report.helper.reportDates import ReportDates
from report.helper.reportMonths import ReportMonths
from report.helper.manager import ReportManager

from aws.collector import Collector as awsCollector
from heroku.collector import Collector as herokuCollector
from gds.collector import Collector as GDSCollector


from aws.forecast import Forecast as awsForecast
from heroku.forecast import Forecast as herokuForecast
from gds.forecast import Forecast as gdsForecast

class Processor:

    def __init__(self):
        self.reportDates = ReportDates()
        self.reportManager = ReportManager()
        self.__setReportDates()
    
    def __setReportDates(self):
        for month in ReportMonths:
            month,start_date,end_date = ReportDates().startAndendDateForMonth(month=month.value)
            self.reportManager.updateReportDate(month=month,start_date=start_date,end_date=end_date)

    def __awsCollector(self):
        report_dates = self.reportManager.reportDates()
        linked_accounts_start_date = self.reportManager.reportDatesByMonth(ReportMonths.CURRENT_MONTH_MINUS_6.value)[0].start_date
        linked_accounts_end_date = self.reportManager.reportDatesByMonth(ReportMonths.CURRENT_MONTH.value)[0].end_date
        
        awsCollector().run(report_dates=report_dates,linked_accounts_start_date=linked_accounts_start_date,linked_accounts_end_date=linked_accounts_end_date)
    
    def __herokuCollector(self):
        report_dates = self.reportManager.reportDates()
        herokuCollector().run(report_dates=report_dates)

    def __gdsCollector(self):
        report_dates = self.reportManager.reportDates()
        GDSCollector().run(report_dates=report_dates)
    
    
    def runCollectors(self):
        self.__awsCollector()
        self.__gdsCollector()
        self.__herokuCollector()
       
    
    def runForecasters(self):
        awsForecast()
        gdsForecast()
        herokuForecast()
        