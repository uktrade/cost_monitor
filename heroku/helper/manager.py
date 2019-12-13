
from heroku.models import HerokuTeam, HerokuCost


class HerokuRecordManager:

  
    def getHerokuTeam(self, team):
        return HerokuTeam.objects.filter(name=team)

    def getHerokuTeams(self):
        return HerokuTeam.objects.all()

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
