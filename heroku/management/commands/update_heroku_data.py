from django.core.management.base import BaseCommand
from  heroku.collector import Collector
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Collector().run()
            self.stdout.write(self.style.SUCCESS("Heroku: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
