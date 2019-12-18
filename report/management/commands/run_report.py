from django.core.management.base import BaseCommand
from report.processor import Processor
from report.helper.export.prometheus import Prometheus

import traceback
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.perf_counter()
        processor = Processor()
        try:
            processor.runCollectors()
            processor.runForecasters()
            self.stdout.write(self.style.SUCCESS("Report Execusion: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()

        run_time = time.perf_counter() - start_time

        self.stdout.write(self.style.SUCCESS(f'run time: {run_time}'))