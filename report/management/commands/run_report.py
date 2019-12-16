from django.core.management.base import BaseCommand
from report.processor import Processor
import traceback
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.perf_counter()

        try:
            Processor().runCollectors()
            Processor().runForecasters()
            self.stdout.write(self.style.SUCCESS("Report Execusion: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()

        run_time = time.perf_counter() - start_time

        self.stdout.write(self.style.SUCCESS(f'run time: {run_time}'))