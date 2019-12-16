from django.core.management.base import BaseCommand
from report.processor import Processor
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Processor().runCollectors()
            Processor().runForecasters()
            self.stdout.write(self.style.SUCCESS("Report: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
