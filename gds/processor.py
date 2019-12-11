
from gds.helper.db import GDSRecordManager
from gds.helper.api import Client
from django.conf import settings


class Processor:

    def __init__(self):

        self.gds_record_mananger = GDSRecordManager()
        self.gds_cleint = Client(gds_api_url=settings.GDS_PAAS_API_URL, gds_billing_url=settings.GDS_BILLING_API_URL,
                                 login_name=settings.GDS_USER, password=settings.GDS_USER_PASS)
        self.dateformat = '%Y-%m-%d'

    def run(self):

        self.gds_cleint.setAccessToken()

        self.gds_record_mananger.updateGDSDates()

        dates = self.gds_record_mananger.getGDSReportDates()

        self.gds_record_mananger.updateOrganizations(
            organizations=self.gds_cleint.getOrganizations())

        organizations = self.gds_record_mananger.getOgranizations()

        for date in dates:
            start_date = date.start_date.strftime(self.dateformat)
            end_date = date.end_date.strftime(self.dateformat)
            for organization in organizations:
                organization_bill = self.gds_cleint.getOrganizationBills(
                    organization_id=organization.id, start_date=start_date, end_date=end_date)

                spaces = []

                for space in organization_bill:
                    # appending space id and name
                    spaces.append(tuple([space[0], space[1]]))

                # Update Organization Spaces
                self.gds_record_mananger.updateOrganizationSpaces(
                    organization=organization, spaces=spaces)

                # Update Space Cost
                for space_id, space_name, amount in organization_bill:
                    space = self.gds_record_mananger.getSpaceById(
                        space_id=space_id)[0]

                    self.gds_record_mananger.updateCost(
                        date=date, organization=organization, space=space, amount=amount)
