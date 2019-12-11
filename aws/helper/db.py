from forecast.helper.date import Ranges
from aws.models import AwsReportDates, AwsAccounts, AwsAccountCost


class AwsRecordManager:

    def getAwsReportDates(self):
        return AwsReportDates.objects.order_by('-month')

    def getLinkedAccountsbyDate(self, date):
        return AwsAccounts.objects.filter(report_date=date)

    def updateAwsDates(self):
        dates = set(Ranges().past_6_months(aws=True))
        dates_in_db = self.getAwsReportDates()
        update_dates = dates.difference(dates_in_db)

        if dates_in_db:
            for month, start_date, end_date in update_dates:
                AwsReportDates.objects.filter(month=month).update(
                    start_date=start_date, end_date=end_date)
        else:
            for month, start_date, end_date in update_dates:
                AwsReportDates.objects.create(
                    month=month, start_date=start_date, end_date=end_date)

    def updateLinkedAcounts(self, date, linked_accounts):
        for id, name in linked_accounts:
            AwsAccounts.objects.update_or_create(
                report_date=date, id=id, name=name)

    def updateCost(self, date, bills):

        linked_accounts = self.getLinkedAccountsbyDate(date=date)

        for account_id, amount in bills:
            linked_account = linked_accounts.filter(id=account_id)[0]
            AwsAccountCost.objects.update_or_create(
                account=linked_account, amount=amount)
