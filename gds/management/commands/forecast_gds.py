from django.core.management.base import BaseCommand
from gds.forecast import Forecast
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Forecast()
            self.stdout.write(self.style.SUCCESS("GDS: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
