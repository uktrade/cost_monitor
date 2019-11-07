import requests
from requests.exceptions import HTTPError


class client:

    def __init__(self, gds_api_url=None, gds_billing_url=None, login_name=None, password=None):
        self.gds_api_url = gds_api_url
        self.gds_billing_url = gds_billing_url
        self.login_name = login_name
        self.password = password
        self.access_token = None

    def __getRequest(self, uri=None, headers=dict(), query=dict()):
        headers['User-Agent'] = 'DIT Billing API Client'
        return requests.get(uri, headers=headers, params=query)

    def __postRequest(self, uri=None, headers=dict(), data=dict()):
        headers['User-Agent'] = 'DIT Billing API Client'
        return requests.post(uri, headers=headers, data=data)

    def getLoginLink(self):
        apiInfo = self.__getRequest("{}/info".format(self.gds_api_url))
        return apiInfo.json()['authorization_endpoint'] + '/oauth/token'

    def setAccessToekn(self):
        loginLink = self.getLoginLink()

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

    def getOrgs(self):
        organizations = list()
        headers = {
            'Accept': 'application/json',
            'Authorization': "Bearer {}".format(self.access_token)
        }
        orgsLink = self.gds_api_url + '/v3/organizations'

        while True:
            orgInfo = self.__getRequest(uri=orgsLink, headers=headers).json()
            for org in orgInfo['resources']:
                organizations.append(
                    {'name': org['name'], 'guid': org['guid']})
            if 'next' not in orgInfo['pagination'].keys():
                break
            orgsLink = ['pagination']['next']

        return organizations

    def get_bill(self, start_date=None, end_date=None):
        billing_data = dict()
        headers = {
            'Accept': 'application/json',
            'Authorization': "Bearer {}".format(self.access_token)
        }

        query = {
            'range_start': start_date,
            'range_stop': end_date
        }

        for org in self.getOrgs():
            query['org_guid'] = org['guid']
            billingInfo = self.__getRequest(
                self.gds_billing_url, headers=headers, query=query).json()
            space_bill = dict()
            for bill in billingInfo:
                space_name = bill['space_name']
                if space_name not in space_bill.keys():
                    space_bill[space_name] = 0
                else:
                    space_bill[space_name] += float(bill['price']['inc_vat'])
            org_total = 0
            for space_name, bill in space_bill.items():
                org_total += bill
                billing_data["{}/{}".format(org['name'], space_name)] = bill

            billing_data["{}/ALl SPACES".format(org['name'])] = org_total

        return billing_data
