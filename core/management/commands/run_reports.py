from django.core.management.base import BaseCommand
import traceback
from core.helper.report import Forecast
from core.helper.gecko import cleint as gecko_client


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            forecast = Forecast()
            reporter = gecko_client()
            reporter.push(widget_uuid="112259-c042ad20-69ee-0137-9497-02bceabe9fa6",
                          payload=reporter.leaderboard_format(forecast.aws()))

            reporter.push(widget_uuid="112259-ee70f130-69ee-0137-3a04-0eef46684bc6",
                          payload=reporter.leaderboard_format(
                              forecast.heroku()))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
