import requests
import re
from bs4 import BeautifulSoup


class client:
    def __init__(self, site=None, login_site=None, login_name=None, password=None):
        self.site = site
        self.login_name = login_name
        self.password = password
        self.login_site = login_site
        self.webClient = requests.session()
        self.webClient.cookies.clear()
        self.csrftoken = None
        self.login_success = dict()
        self.org_data = list()

    def __soup(self, data):
        return BeautifulSoup(data, 'html.parser')

    def login(self):

        try:
            response = self.webClient.get(self.site)
            self.csrftoken = self.webClient.cookies['X-Uaa-Csrf']

            action = (self.__soup(response.content)).form.get('action')

            login_form = self.login_site + action
            login_data = {
                'username': self.login_name,
                'password': self.password,
                'X-Uaa-Csrf': self.csrftoken
            }

            login_response = self.webClient.post(login_form, login_data)
            match_groups = re.match(
                'https?:\/\/(.+)(\/.*)', login_response.url)
            url = match_groups[0]
            host = match_groups[1]
            path = match_groups[2]

            match_expected_response_url = re.match('^admin', host)

            if match_expected_response_url is None:
                raise RuntimeError('Login Failed')

            self.login_success = {'url': url, 'host': host, 'path': path}

        except Exception as e:
            raise e

    def __get_orgs(self):
        response = self.webClient.get(self.login_success['url'])

        for link in (self.__soup(response.content)).find_all('a'):
            if re.match(self.login_success['path'], link.get('href')):
                self.org_data.append({'name': (link.get_text()).strip(
                ), 'link': 'https://' + self.login_success['host'] + link.get('href')})

    def __get_org_spaces(self):

        for org in self.org_data:
            response = self.webClient.get(org['link'])
            spaces = list()
            for link in (self.__soup(response.content)).find_all('a'):
                if link.get('id'):
                    id = (link.get('id')).split('space-')[1]
                    for h3 in link.find_all('h3'):
                        regex = re.compile('[^a-zA-Z:\-0-9]')
                        text = regex.sub('', h3.get_text())
                        spaces.append(
                            {'name': text.split(':')[1], 'id': id, 'bill': 0.0})
                        org.update({'spaces': spaces})

    def get_bill(self, start_date):
        billing_data = dict()
        self.__get_orgs()
        self.__get_org_spaces()
        for org in self.org_data:
            for space in org['spaces']:
                billing_link = org['link'] + '/statements/' + start_date + '?_csrf=' + \
                    self.csrftoken + '&space=' + \
                    space['id'] + '&service=none&sort=name&order=asc'

                space_bill = float()
                response = self.webClient.get(billing_link)
                regex = re.compile('[^0-9\.]')
                for table_header in self.__soup(response.content).find_all('th'):
                    text = table_header.get_text().strip()
                    match = regex.sub('', text)
                    if match:
                        space_bill = float(match)

                billing_data["{}/{}".format(org['name'],
                                            space['name'])] = space_bill

        return billing_data
