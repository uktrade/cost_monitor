import requests


class Client(object):

    def __init__(self, heroku_api_key=None, heroku_site=None):
        self.heroku_api_key = heroku_api_key
        self.heroku_site = heroku_site
        self.headers = {'Accept': 'application/vnd.heroku+json; version=3',
                        'Authorization': 'Bearer ' + self.heroku_api_key}
        self.webclient = requests.Session()
        self.webclient.headers.update(self.headers)

    def __fetch(self, end_point):
        "fetch data from the supplied end point and return the json"
        url = self.heroku_site + '/' + end_point
        response = self.webclient.get(url)
        return response.json()

    def getTeams(self):
        teams = list()
        team_data = self.__fetch(end_point='teams')

        for team in team_data:
            teams.append(team['name'])

        return teams

    def getBills(self,teams,start_date):
        billing_data = []
        for team in teams:
            invoice_list = self.__fetch("teams/%s/invoices" % team)
            for invoice in invoice_list:
                if invoice['period_start'] == start_date:
                    amount = invoice['total'] / 100
                else:
                    amount = 0.0
            billing_data.append(tuple([team,float(amount)]))

        return billing_data
