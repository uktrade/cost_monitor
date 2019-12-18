from aws.models import AwsAccount, AwsAccountCost, AwsForecast, AwsTeamAccountAssociation
from report.models import ReportDate


class AwsRecordManager:

    def getLinkedAccounts(self):
        return AwsAccount.objects.all()

    def getLinkedAccountbyID(self, id):
        return self.getLinkedAccounts().filter(id=id)

    def getLinkedAccountByName(self, name):
        return self.getLinkedAccounts().filter(name=name)

    def getAssociatedTeamByAccountName(self, account_name):
        return AwsTeamAccountAssociation.objects.filter(account_name=account_name)

    def getCost(self):
        return AwsAccountCost.objects.all()

    def getCostByMonth(self, month):
        report_date = ReportDate.objects.filter(month=month)[0]
        return AwsAccountCost.objects.filter(report_date=report_date).all()

    def getCostByMonthAndAccountID(self, month, account_id):
        account = self.getLinkedAccountbyID(id=account_id)[0]
        report_date = ReportDate.objects.filter(month=month)[0]
        return AwsAccountCost.objects.filter(report_date=report_date, account=account)

    def getForecast(self):
        return AwsForecast.objects.all()

    def updateLinkedAcounts(self, linked_accounts):

        linked_accounts_in_db = set(self.getLinkedAccounts().values_list())
        linked_accounts = set(linked_accounts)

        add_accounts = linked_accounts.difference(linked_accounts_in_db)
        remove_accounts = linked_accounts_in_db.difference(linked_accounts)

        for id, name in remove_accounts:
            AwsAccount.objects.filter(id=id).delete()

        for id, name in add_accounts:
            AwsAccount.objects.create(id=id, name=name)

    def updateAccountTeamAssociation(self, suggested_team_names):
        for account_name, team_name in suggested_team_names:
            if not self.isAccountInTeamAssociation(account_name=account_name):
                account = self.getLinkedAccountByName(name=account_name)[0]
                AwsTeamAccountAssociation.objects.create(
                    account=account, account_name=account_name, team=team_name)

    def updateCost(self, date, bills):

        for account_id, amount in bills:
            linked_account = self.getLinkedAccountbyID(id=account_id)[0]
            AwsAccountCost.objects.update_or_create(
                report_date=date, account=linked_account, amount=amount)

    def updateForecast(self, forecastData):
        for forecast in forecastData:
            cost_id = self.getCostByMonthAndAccountID(
                month=0, account_id=forecast['id'])[0]
            AwsForecast.objects.update_or_create(
                cost_id=cost_id, amount=forecast['amount'], difference=forecast['difference'])

    def isAccountInTeamAssociation(self, account_name):
        if AwsTeamAccountAssociation.objects.filter(account_name=account_name):
            return True
        return False
