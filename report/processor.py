from report.helper.reportDates import ReportDates
from report.helper.reportMonths import ReportMonths
from report.helper.manager import ReportManager

from aws.collector import Collector as awsCollector
from heroku.collector import Collector as herokuCollector
from gds.collector import Collector as GDSCollector

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


    def __awsForecast(self):
        pass
    
    def runCollectors(self):
        self.__awsCollector()
        self.__herokuCollector()
        self.__gdsCollector()

    
    def runForecasters(self):
        self.__awsForecast()
        # awsManager = AwsRecordManager()

        # for date in awsManager.getAwsReportDates():
        #     print(date.month)

            # def __init__(self):
            #     self.aws = AwsRecordManager()
            #     self.gds = GDSRecordManager()
            #     self.
            #     self.dateformat = '%Y-%m-%d'

            # def heroku(self):

            #     this_month_start_date = (Ranges().current_month())['start_date']
            #     previous_month_start_date = (Ranges().previous_month())['start_date']

            #     hc = heroku_client(heroku_api_key=settings.HEROKU_API_KEY,
            #                        heroku_site=settings.HEROKU_SITE)

            #     this_month_bill = hc.get_bill(
            #         start_date=this_month_start_date.strftime(self.dateformat))

            #     previous_month_bill = hc.get_bill(
            #         start_date=previous_month_start_date.strftime(self.dateformat))

            #     return self.__forecast(this_month=this_month_bill,
            #                            previous_month=previous_month_bill)

            # def aws(self):
            #     this_month_dates = Ranges().current_month(aws=True)
            #     previous_month_dates = Ranges().previous_month(aws=True)

            #     ac = boto_aws_client(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            #                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            #     this_month_bill = ac.get_bill(
            #         start_date=this_month_dates['start_date'].strftime(self.dateformat), end_date=this_month_dates['end_date'].strftime(self.dateformat))

            #     previous_month_bill = ac.get_bill(
            #         start_date=previous_month_dates['start_date'].strftime(self.dateformat), end_date=previous_month_dates['end_date'].strftime(self.dateformat))

            #     return self.__forecast(this_month=this_month_bill,
            #                            previous_month=previous_month_bill)

            # def gds_paas_bill_forecat(self):
            #     this_month_dates = Ranges().current_month()
            #     previous_month_dates = Ranges().previous_month()

            #     gc = gds_api_client(gds_api_url=settings.GDS_PAAS_API_URL,
            #                         gds_billing_url=settings.GDS_BILLING_API_URL,
            #                         login_name=settings.GDS_USER,
            #                         password=settings.GDS_USER_PASS)

            #     gc.setAccessToken()
            #     this_month_bill = gc.get_bill(start_date=this_month_dates['start_date'].strftime(self.dateformat),
            #                                   end_date=this_month_dates['end_date'].strftime(
            #                                       self.dateformat)
            #                                   )
            #     previous_month_bill = gc.get_bill(start_date=previous_month_dates['start_date'].strftime(self.dateformat),
            #                                       end_date=previous_month_dates['end_date'].strftime(
            #         self.dateformat)
            #     )

            #     return self.__forecast(this_month_bill, previous_month_bill)

            # def __forecast(self, this_month=None, previous_month=None):
            #     forecast_data = list()
            #     day = self.dates.today.day

            #     number_of_days_this_month = self.dates.number_of_days_in_current_month()

            #     this_month_accounts = list(this_month.keys())
            #     previous_month_accounts = list(previous_month.keys())

            #     accounts = set(this_month_accounts + previous_month_accounts)

            #     total_forecast = 0.0

            #     for account in accounts:
            #         percent_diff = None
            #         forecast = None
            #         if account in previous_month_accounts and account not in this_month_accounts:
            #             pass
            #         else:
            #             this_month_bill = this_month[account]

            #             forecast = (this_month_bill / day) * number_of_days_this_month
            #             forecast = float(format(forecast, '.2f'))
            #             if account not in previous_month_accounts and account in this_month_accounts:
            #                 percent_diff = 0.0

            #             else:
            #                 if account in previous_month_accounts and account in this_month_accounts:
            #                     previous_bill = previous_month[account]
            #                     if previous_bill > 0:
            #                         diff = (forecast - previous_bill) / previous_bill
            #                         percent_diff = diff * 100
            #                     else:
            #                         percent_diff = 0.0

            #             forecast_data.append({'name': account, 'forecast': float(
            #                 format(forecast, '.2f')), 'percent_diff': float(format(percent_diff, '.2f'))})

            #     forecast_data = sorted(
            #         forecast_data, key=itemgetter('forecast'), reverse=True)

            #     return forecast_data
