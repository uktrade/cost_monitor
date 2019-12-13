from gds.models import GDSOrganization, GDSOrganizationsSpace, GDSCost


class GDSRecordManager:

    def getOgranizations(self):
        return GDSOrganization.objects.all()

    def getOrganizationById(self, organization_id):
        return self.getOgranizations().filter(id=organization_id)

    def getSpaces(self):
        return GDSOrganizationsSpace.objects.all()

    def getSpaceById(self, space_id):
        return self.getSpaces().filter(id=space_id)

    def getOrganizationSpaces(self, organization_id):
        orgnization_obj = self.getOrganizationById(
            organization_id=organization_id)[0]
        return self.getSpaces().filter(organization_id=orgnization_obj)

    def getOrganizationSpaceById(self, organization_id, space_id):
        orgnization_obj = self.getOrganizationById(
            organization_id=organization_id)[0]
        return self.getSpaces().filter(organization_id=orgnization_obj, id=space_id)


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
