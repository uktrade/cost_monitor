
from gds.helper.manager import GDSRecordManager
from gds.helper.api import Client
from django.conf import settings


class Collector:

    def __init__(self):

        self.gdsManager = GDSRecordManager()
        self.gdsClient = Client(gds_api_url=settings.GDS_PAAS_API_URL, gds_billing_url=settings.GDS_BILLING_API_URL,
                                 login_name=settings.GDS_USER, password=settings.GDS_USER_PASS)
        self.dateformat = '%Y-%m-%d'

    def run(self,report_dates):

        self.gdsClient.setAccessToken()
        self.gdsManager.updateOrganizations(
            organizations=self.gdsClient.getOrganizations())

        for date in report_dates:
            start_date = date.start_date.strftime(self.dateformat)
            end_date = date.end_date.strftime(self.dateformat)
            
            for organization in self.gdsManager.getOgranizations():
                organization_bill = self.gdsClient.getOrganizationBills(
                    organization_id=organization.id, start_date=start_date, end_date=end_date)

                spaces = []

                for space in organization_bill:
                    # appending space id and name
                    spaces.append(tuple([space[0], space[1]]))

                # Update Organization Spaces
                self.gdsManager.updateOrganizationSpaces(
                    organization=organization, spaces=spaces)

                # Update Space Cost
                for space_id, space_name, amount in organization_bill:
                    space = self.gdsManager.getSpaceById(
                        space_id=space_id)[0]

                    self.gdsManager.updateCost(
                        date=date, organization=organization, space=space, amount=amount)