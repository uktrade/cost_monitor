
from operator import itemgetter
from django.conf import settings
from core.helper.date import Ranges
from heroku.helper.api import client as heroku_client
from aws.helper.api import client as boto_aws_client


class Forecast:

    def __init__(self):
        self.dates = Ranges()
        self.dateformat = '%Y-%m-%d'

    def heroku(self):

        this_month_start_date = (Ranges().current_month())['start_date']
        previous_month_start_date = (Ranges().previous_month())['start_date']

        hc = heroku_client(heroku_api_key=settings.HEROKU_API_KEY,
                           heroku_site=settings.HEROKU_SITE)

        this_month_bill = hc.get_bill(
            start_date=this_month_start_date.strftime(self.dateformat))

        previous_month_bill = hc.get_bill(
            start_date=previous_month_start_date.strftime(self.dateformat))

        return self.__forecast(this_month=this_month_bill,
                               previous_month=previous_month_bill)

    def aws(self):
        this_month_dates = Ranges().current_month(aws=True)
        previous_month_dates = Ranges().previous_month(aws=True)

        ac = boto_aws_client(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        this_month_bill = ac.get_bill(
            start_date=this_month_dates['start_date'].strftime(self.dateformat), end_date=this_month_dates['end_date'].strftime(self.dateformat))

        previous_month_bill = ac.get_bill(
            start_date=previous_month_dates['start_date'].strftime(self.dateformat), end_date=previous_month_dates['end_date'].strftime(self.dateformat))

        return self.__forecast(this_month=this_month_bill,
                               previous_month=previous_month_bill)

    def __forecast(self, this_month=None, previous_month=None):
        forecast_data = list()
        day = self.dates.today.day

        number_of_days_this_month = self.dates.number_of_days_in_current_month()

        this_month_accounts = list(this_month.keys())
        previous_month_accounts = list(previous_month.keys())

        accounts = set(this_month_accounts + previous_month_accounts)

        total_forecast = 0.0

        for account in accounts:
            percent_diff = None
            forecast = None
            if account in previous_month_accounts and account not in this_month_accounts:
                pass
            else:
                this_month_bill = this_month[account]

                forecast = (this_month_bill / day) * number_of_days_this_month
                forecast = float(format(forecast, '.2f'))
                if account not in previous_month_accounts and account in this_month_accounts:
                    percent_diff = 0.0

                else:
                    if account in previous_month_accounts and account in this_month_accounts:
                        previous_bill = previous_month[account]
                        if previous_bill > 0:
                            diff = (forecast - previous_bill) / previous_bill
                            percent_diff = diff * 100
                        else:
                            percent_diff = 0.0

            forecast_data.append({'name': account, 'forecast': float(
                format(forecast, '.2f')), 'percent_diff': float(format(percent_diff, '.2f'))})

        forecast_data = sorted(
            forecast_data, key=itemgetter('forecast'), reverse=True)

        return forecast_data
