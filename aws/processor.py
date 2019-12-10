
from aws.helper.db import AwsRecordManager
from aws.helper.api import Client


class Processor:

    def __init__(self):

        self.aws_record_mananger = AwsRecordManager()
        self.aws_cleint = Client()
        self.dateformat = '%Y-%m-%d'

    def run(self):
        self.aws_record_mananger.updateAwsDates()

        dates = self.aws_record_mananger.getAwsReportDates()

        for date in dates:
            start_date = date.start_date.strftime(self.dateformat)
            end_date = date.end_date.strftime(self.dateformat)
            linked_accounts = self.aws_cleint.aws_linked_accounts(
                start_date=start_date, end_date=end_date)


            self.aws_record_mananger.updateLinkedAcounts(date=date,linked_accounts=linked_accounts)
            

            monthly_bills = self.aws_cleint.aws_account_bill(start_date=start_date,end_date=end_date)

            self.aws_record_mananger.updateCost(date=date,bills=monthly_bills)