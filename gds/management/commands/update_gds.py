from django.core.management.base import BaseCommand
import traceback
from core.helper.report import Forecast
from core.helper.gecko import cleint as gecko_client


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            forecast = Forecast()
            reporter = gecko_client()

            payload = reporter.leaderboard_format(
                forecast.gds_paas_bill_forecat())
            reporter.push(widget_uuid="112259-1edb3d60-6ae1-0137-d660-022d23d9b2a0",
                          payload=payload)
            self.stdout.write(self.style.SUCCESS("GDS: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
