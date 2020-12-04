
from aws.helper.manager import AwsRecordManager
from aws.helper.api import Client
from django.conf import settings


class Collector:

    def __init__(self):

        self.awsManager = AwsRecordManager()
        self.awsCleint = Client(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        self.dateformat = '%Y-%m-%d'

    def run(self, report_dates, linked_accounts_start_date, linked_accounts_end_date):

        linked_accounts = self.awsCleint.aws_linked_accounts(start_date=linked_accounts_start_date.strftime(self.dateformat),
                                                             end_date=linked_accounts_end_date.strftime(self.dateformat))

        self.awsManager.updateLinkedAcounts(linked_accounts=linked_accounts)

        suggested_team_names = self.awsCleint.suggestTeamNames(
            linked_accounts=linked_accounts)

        self.awsManager.updateAccountTeamAssociation(
            suggested_team_names=suggested_team_names)

        for date in report_dates:
            #Update cost for current month on each run and, for previous month only if it does not exist already
            if date.month == 0 or not self.awsManager.getCostByMonth(month=date.month):
                start_date = date.start_date.strftime(self.dateformat)
                end_date = date.end_date.strftime(self.dateformat)
                monthly_bills = self.awsCleint.aws_account_bill(
                    start_date=start_date, end_date=end_date)
                self.awsManager.updateCost(date=date, bills=monthly_bills)
