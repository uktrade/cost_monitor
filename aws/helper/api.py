import boto3


class client:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
        self.client = session.client('ce')

    def __get_linked_accounts(self, start_date, end_date):
        linked_accounts_map = {}
        accounts_data = dict()
        linked_accounts_map = dict()

        accounts_data = self.client.get_dimension_values(TimePeriod={
                                                         'Start': start_date, 'End': end_date}, Dimension='LINKED_ACCOUNT')['DimensionValues']

        if accounts_data:
            for account in accounts_data:
                linked_accounts_map.update(
                    {account['Value']: account['Attributes']['description']})

        return linked_accounts_map

    def get_bill(self, start_date, end_date):
        billing_response = None
        linked_accounts_map = self.__get_linked_accounts(
            start_date, end_date)
        billing_data = dict()

        billing_response = self.client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY', Metrics=[
            'UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}])['ResultsByTime'][0]['Groups']

        for bill in billing_response:
            id = bill['Keys'][0]
            name = linked_accounts_map[id]
            amount = bill['Metrics']['UnblendedCost']['Amount']
            billing_data[name] = float(amount)

        return billing_data
