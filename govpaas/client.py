from urllib.parse import urljoin

import requests


class Client:
    _token = None
    _api_url = None
    _billing_url = None
    _access_token = None

    _default_headers = {"User-Agent": "DIT-Billing-API-Client"}

    def __init__(self, api_url, billing_url, username=None, password=None):
        self._api_url = api_url
        self._billing_url = billing_url

        if username and password:
            self.authenticate(username, password)

    def _auth_headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._access_token}",
            **self._default_headers,
        }

    def get_auth_url(self):
        api_info_url = urljoin(self._api_url, "info")

        response = requests.get(api_info_url)

        auth_url = response.json()["authorization_endpoint"]

        return urljoin(auth_url, "/oauth/token")

    def authenticate(self, username, password):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Authorization": "Basic Y2Y6",
            **self._default_headers,
        }

        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }

        response = requests.post(self.get_auth_url(), data=data, headers=headers)
        self._access_token = response.json()['access_token']

    def get_orgs(self):
        """Return a list of orgs"""

        url = urljoin(self._api_url, "/v3/organizations")

        response = requests.get(url, headers=self._auth_headers())

        response_data = response.json()

        # the endpoint supports pagination but we don't expect to ever
        # have to use pagination
        assert not response_data["pagination"]["next"]

        return response_data["resources"]

    def get_billing_data(self, org_guid, start_date, end_date):
        """Return billing data for an org"""

        data = {
            "range_start": start_date,
            "range_stop": end_date,
            "org_guid": org_guid,
        }

        response = requests.get(url=self._billing_url, params=data, headers=self._auth_headers())
        return response.json()
