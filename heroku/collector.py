
from heroku.helper.manager import HerokuRecordManager
from heroku.helper.api import Client
from django.conf import settings


class Collector:

    def __init__(self):

        self.herokuManager = HerokuRecordManager()
        self.herokuClient = Client(
            heroku_api_key=settings.HEROKU_API_KEY, heroku_site=settings.HEROKU_SITE)
        self.dateformat = '%Y-%m-%d'

    def run(self,report_dates):
       
        teams = self.herokuClient.getTeams()
        self.herokuManager.updateHerokuTeam(teams=teams)


        for date in report_dates:
            teams_in_db = self.herokuManager.getHerokuTeams()
           
            monthly_bills = self.herokuClient.getBills(
                teams=teams_in_db, start_date=date.start_date.strftime(self.dateformat))
            self.herokuManager.updateCost(
                date=date, bills=monthly_bills)
