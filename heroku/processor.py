
from heroku.helper.db import HerokuRecordManager
from heroku.helper.api import Client
from django.conf import settings

class Processor:

    def __init__(self):

        self.heroku_record_mananger = HerokuRecordManager()
        self.heroku_cleint = Client(heroku_api_key=settings.HEROKU_API_KEY,heroku_site=settings.HEROKU_SITE)

    def run(self):
        self.heroku_record_mananger.updateHerokuDates()
        
        teams = self.heroku_cleint.getTeams()
        self.heroku_record_mananger.updateHerokuTeam(teams=teams)

        dates = self.heroku_record_mananger.getHerokuReportDates() 

        for date in dates:

            monthly_bills = self.heroku_cleint.getBills(teams=teams,start_date=date.start_date)
            self.heroku_record_mananger.updateCost(date=date,bills=monthly_bills)