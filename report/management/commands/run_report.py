from django.core.management.base import BaseCommand
from report.processor import Processor

import traceback
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.perf_counter()
        processor = Processor()
        try:
            processor.setReportDates()
            processor.runCollectors()
            processor.runForecasters()
            processor.exportAwsForecastToGeckoboard(widget_uuid="112259-c042ad20-69ee-0137-9497-02bceabe9fa6")
            processor.exportGDSForecastToGeckoboard(widget_uuid="112259-ee70f130-69ee-0137-3a04-0eef46684bc6")
            self.stdout.write(self.style.SUCCESS("Report Execusion: OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()

        run_time = time.perf_counter() - start_time

        self.stdout.write(self.style.SUCCESS(f'run time: {run_time}'))
