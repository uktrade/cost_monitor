from gds.models import GDSOrganization, GDSOrganizationsSpace, GDSCost, GDSForecast, GDSTeamSpaceAssociation
from report.models import ReportDate


class GDSRecordManager:

    def getOgranizations(self):
        return GDSOrganization.objects.all()

    def getOrganizationById(self, organization_id):
        return self.getOgranizations().filter(id=organization_id)

    def getSpaces(self):
        return GDSOrganizationsSpace.objects.all()

    def getSpaceById(self, space_id):
        return self.getSpaces().filter(id=space_id)

    def getSpaceByName(self, name):
        return self.getSpaces().filter(name=name)

    def getAssociatedTeamNameBySpaceName(self, space_name):
        return GDSTeamSpaceAssociation.objects.filter(space_name=space_name)

    def getOrganizationSpaces(self, organization_id):
        orgnization_obj = self.getOrganizationById(
            organization_id=organization_id)[0]
        return self.getSpaces().filter(organization_id=orgnization_obj)

    def getOrganizationSpaceById(self, organization_id, space_id):
        orgnization_obj = self.getOrganizationById(
            organization_id=organization_id)[0]
        return self.getSpaces().filter(organization_id=orgnization_obj, id=space_id)

    def getCost(self):
        return GDSCost.objects.all()

    def getCostByMonth(self, month):
        report_date = ReportDate.objects.filter(month=month)[0]
        return GDSCost.objects.filter(report_date=report_date).all()

    def getCostByMonthAndSpaceID(self, month, space_id):
        report_date = ReportDate.objects.filter(month=month)[0]
        space_obj = self.getSpaceById(space_id=space_id)[0]
        return GDSCost.objects.filter(report_date=report_date, space_id=space_obj)

    def getForecast(self):
        return GDSForecast.objects.all()

    def updateOrganizations(self, organizations):
        organizations_in_db = set(self.getOgranizations().values_list())
        organizations = set(organizations)

        add_organization = organizations.difference(organizations_in_db)
        remove_organizations = organizations_in_db.difference(organizations)

        for organization_id, organization_name in remove_organizations:
            GDSOrganization.objects.filter(id=organization_id).delete()

        for organization_id, organization_name in add_organization:
            GDSOrganization.objects.create(
                id=organization_id, name=organization_name)

    def updateOrganizationSpaces(self, organization, spaces):

        spaces_in_db = set(self.getOrganizationSpaces(
            organization_id=organization.id).values_list('id', 'name'))

        spaces = set(spaces)

        add_spaces = spaces.difference(spaces_in_db)
        remove_spaces = spaces_in_db.difference(spaces)

        for space_id, space_name in remove_spaces:
            GDSOrganizationsSpace.objects.filter(id=space_id).delete()

        for space_id, space_name in add_spaces:
            GDSOrganizationsSpace.objects.create(
                organization_id=organization, id=space_id, name=space_name)

    def updateCost(self, date, organization, space, amount):
        GDSCost.objects.update_or_create(
            report_date=date, organization_id=organization, space_id=space, amount=amount)

    def updateTeamSpaceAssociation(self, suggested_team_names):
        for space_name, team_name in suggested_team_names:
            if not self.isSpaceInTeamAssociation(space_name=space_name):
                space = self.getSpaceByName(name=space_name)[0]
                GDSTeamSpaceAssociation.objects.create(
                    space=space, space_name=space_name, team=team_name)

    def updateForecast(self, forecastData):
        for forecast in forecastData:
            cost_id = self.getCostByMonthAndSpaceID(
                month=0, space_id=forecast['id'])[0]
            GDSForecast.objects.update_or_create(
                cost_id=cost_id, amount=forecast['amount'], difference=forecast['difference'])

    def isSpaceInTeamAssociation(self, space_name):
        if GDSTeamSpaceAssociation.objects.filter(space_name=space_name):
            return True
        return False
