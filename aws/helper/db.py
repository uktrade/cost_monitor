from core.helper.date import Ranges
from aws.models import AwsReportDates, AwsAccounts, AccountsCost


class AwsRecordManager:

    def getAwsReportDates(self):
        return AwsReportDates.objects.order_by('-month').values_list()

    def getLinkedAccounts(self):
        return AwsAccounts.objects.order_by('id').values_list()

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

    def upDateLinkedAcounts(self, linked_accounts):
        for id, name in linked_accounts:
            AwsAccounts.objects.update_or_create(id=id, name=name)
