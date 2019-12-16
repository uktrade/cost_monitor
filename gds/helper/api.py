import requests
from requests.exceptions import HTTPError


class Client:

    def __init__(self, gds_api_url=None, gds_billing_url=None, login_name=None, password=None):
        self.gds_api_url = gds_api_url
        self.gds_billing_url = gds_billing_url
        self.login_name = login_name
        self.password = password
        self.access_token = None
        self.userAgent = {'User-Agent': 'DIT-Billing-API-Client'}

    def __getRequest(self, uri=None, headers=None, query=None):
        headers = headers or {}
        query = query or {}
        headers.update(self.userAgent)
        return requests.get(uri, headers=headers, params=query)

    def __postRequest(self, uri=None, headers=None, data=None):
        headers = headers or {}
        data = data or {}
        headers.update(self.userAgent)
        return requests.post(uri, headers=headers, data=data)

    def __getLoginLink(self):
        apiInfo = self.__getRequest(f"{self.gds_api_url}/info")
        return apiInfo.json()['authorization_endpoint'] + '/oauth/token'

    def setAccessToken(self):
        loginLink = self.__getLoginLink()

        auth_headers = {
            "accept": "application/json;",
            "content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "authorization": "Basic Y2Y6"
        }
        auth_payload = {'grant_type': 'password',
                        'username': self.login_name, 'password': self.password}

        response = self.__postRequest(
            loginLink, headers=auth_headers, data=auth_payload)

        self.access_token = response.json()['access_token']

    def getOrganizations(self):
        organizations_list = []
        headers = {
            'Accept': 'application/json',
            'Authorization': "Bearer {}".format(self.access_token)
        }
        organizations = f'{self.gds_api_url}/v3/organizations'

        while True:
            organizationsInfo = self.__getRequest(
                uri=organizations, headers=headers).json()

            for organization in organizationsInfo['resources']:
                organizations_list.append(
                    tuple([organization['guid'], organization['name']]))

            if organizationsInfo['pagination']['next'] is None:
                break
            organizations = organizationsInfo['pagination']['next']

        return organizations_list

    def getOrganizationBills(self, organization_id, start_date, end_date):
        billing_data = []
        headers = {
            'Accept': 'application/json',
            'Authorization': "Bearer {}".format(self.access_token)
        }

        query = {
            'range_start': start_date,
            'range_stop': end_date
        }

        query.update({'org_guid': organization_id})

        billingInfo = self.__getRequest(
            uri=self.gds_billing_url, headers=headers, query=query).json()

        space_bill = {}
        for bill in billingInfo:
            space_name = bill['space_name']
            space_id = bill['space_guid']

            if space_name not in space_bill:
                space_bill.update(
                    {space_name: {'guid': space_id, 'amount': 0}})

            amount = space_bill[space_name]['amount'] + \
                float(bill['price']['inc_vat'])

            space_bill.update(
                {space_name: {'guid': space_id, 'amount': amount}})

        for space_name, space_data in space_bill.items():
            billing_data.append(
                tuple([space_data['guid'], space_name, space_data['amount']]))

        return billing_data
