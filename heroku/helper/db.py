from forecast.helper.date import Ranges
from heroku.models import HerokuReportDate, HerokuTeam, HerokuCost


class HerokuRecordManager:

    def getHerokuReportDates(self):
        return HerokuReportDate.objects.order_by('-month')

    def getHerokuTeam(self, team):
        return HerokuTeam.objects.filter(name=team)

    def getHerokuTeams(self):
        return HerokuTeam.objects.all()

    def updateHerokuDates(self):
        dates = set(Ranges().past_6_months(aws=False))
        dates_in_db = self.getHerokuReportDates()
        update_dates = dates.difference(dates_in_db)

        if dates_in_db:
            for month, start_date, end_date in update_dates:
                HerokuReportDate.objects.filter(month=month).update(
                    start_date=start_date)
        else:
            for month, start_date, end_date in update_dates:
                HerokuReportDate.objects.create(
                    month=month, start_date=start_date)

    def updateHerokuTeam(self, teams):
        teams_in_db = set(self.getHerokuTeams().values_list())
        teams = set(teams)

        add_teams = teams.difference(teams_in_db)
        delete_teams = teams_in_db.difference(teams)

        for team in delete_teams:
            HerokuTeam.objects.filter(name=team).delete()

        for team in add_teams:
            HerokuTeam.objects.create(name=team)

    def updateCost(self, date, bills):

        for team, amount in bills:
            team_record = self.getHerokuTeam(team=team)[0]
            HerokuCost.objects.update_or_create(
                report_date=date, team=team_record, amount=amount)
