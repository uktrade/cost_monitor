from django.core.management.base import BaseCommand
from gds.processor import Processor
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Processor().run()
            self.stdout.write(self.style.SUCCESS("GDS: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
