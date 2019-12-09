
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

        for month, start_date, end_date in dates:
            linked_accounts = self.aws_cleint.aws_linked_accounts(
                start_date=start_date.strftime(self.dateformat), end_date=end_date.strftime(self.dateformat))

            self.aws_record_mananger.upDateLinkedAcounts(
                linked_accounts=linked_accounts)
