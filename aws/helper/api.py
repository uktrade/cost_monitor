import boto3


class Client:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
        self.client = session.client('ce')

    def aws_linked_accounts(self, start_date, end_date):
        linked_accounts = []
        accounts_data = {}

        accounts_data = self.client.get_dimension_values(TimePeriod={
                                                         'Start': start_date, 'End': end_date}, Dimension='LINKED_ACCOUNT')['DimensionValues']

        if accounts_data:
            for account in accounts_data:
                account_name = account['Attributes']['description']
                account_id = account['Value']
                linked_accounts.append(tuple([account_id, account_name]))

        return linked_accounts

    def aws_account_bill(self,start_date, end_date):
        billing_response = {}
        billing_data = []

        billing_response = self.client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY', Metrics=[
            'UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}])['ResultsByTime'][0]['Groups']

        for bill in billing_response:
            account_id = bill['Keys'][0]
            amount = float(bill['Metrics']['UnblendedCost']['Amount'])
            billing_data.append(tuple([account_id,amount]))

        return billing_data
