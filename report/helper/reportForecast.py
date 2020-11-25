
from report.helper.reportDates import ReportDates


class Forecast:

    def __init__(self, algo='basic', currentMonthBill=[], previousMonthBill=[]):

        self.report_dates = ReportDates()
        self.forecastData = []

        if algo == 'basic':
            self.forecastData = self.__basic(
                currentMonthBill=currentMonthBill, previousMonthsBill=previousMonthBill)

    def __basic(self, currentMonthBill=[], previousMonthsBill=[]):

        forecastData = []
        day = self.report_dates.today.day
        number_of_days_this_month = self.report_dates.number_of_days_in_current_month()

        currentMonthAccounts = set(currentMonthBill.keys())
        previousMonthAccounts = set(previousMonthsBill.keys())

        newAddedAccounts = currentMonthAccounts.difference(
            previousMonthAccounts)
        removedAccounts = previousMonthAccounts.difference(
            currentMonthAccounts)
        existingAccounts = currentMonthAccounts.intersection(
            previousMonthAccounts)

        # Process account which are in both previous and current month
        for account in existingAccounts:
            percent_diff = None
            forecast = None

            accountCurrentBill = currentMonthBill[account]
            accountPreviousBill = previousMonthsBill[account]

            accountForecast = (accountCurrentBill / day) * \
                number_of_days_this_month

            accountPercentDiff = 0.0

            if accountPreviousBill != 0:
                accountPercentDiff = (
                    accountForecast - accountPreviousBill) / accountPreviousBill

            forecastData.append(
                {'id': account, 'amount': accountForecast, 'difference': accountPercentDiff * 100})

        # process newly added accounts
        for account in newAddedAccounts:
            accountForecast = (
                currentMonthBill[account] / day) * number_of_days_this_month
            accountPercentDiff = 0.00
            forecastData.append(
                {'id': account, 'amount': accountForecast, 'difference': accountPercentDiff})

        return forecastData
