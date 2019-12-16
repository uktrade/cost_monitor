
from heroku.models import HerokuTeam, HerokuCost, HerokuForecast
from report.models import ReportDate

class HerokuRecordManager:


    def getHerokuTeams(self):
        return HerokuTeam.objects.all()

    def getCostByMonth(self,month):
        report_date = ReportDate.objects.filter(month=month)[0]
        return HerokuCost.objects.filter(report_date=report_date)

    def getHerokuTeamByID(self,team_id):
        return HerokuTeam.objects.filter(id=team_id)

    def getCostByMonthAndTeamID(self,month,team_id):
        report_date = ReportDate.objects.filter(month=month)[0]
        team = self.getHerokuTeamByID(team_id=team_id)[0]
        return HerokuCost.objects.filter(report_date=report_date,team=team)

    def updateHerokuTeam(self, teams):
        teams_in_db = set(self.getHerokuTeams().values_list())
        teams = set(teams)

        add_teams = teams.difference(teams_in_db)
        delete_teams = teams_in_db.difference(teams)

        for id,name in delete_teams:
            HerokuTeam.objects.filter(id=id).delete()

        for id,name in add_teams:
            HerokuTeam.objects.create(id=id,name=name)

    def updateCost(self, date, bills):
        for team_id, amount in bills:
            team_record = self.getHerokuTeamByID(team_id=team_id)[0]
            HerokuCost.objects.update_or_create(
                report_date=date, team=team_record, amount=amount)


    def updateForecast(self,forecastData):
        for forecast in forecastData:
            cost_id = self.getCostByMonthAndTeamID(month=0,team_id=forecast['id'])[0]
            HerokuForecast.objects.update_or_create(cost_id=cost_id,amount=forecast['amount'],difference=forecast['difference'])

