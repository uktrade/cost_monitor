from django.views import View
from django.http import HttpResponse

import prometheus_client

from govpaas.models import BillingData
from report.helper.export.prometheus import PrometheusForecast


class PrometheusForecastView(View):

    def get(self, request):
        registry = prometheus_client.CollectorRegistry()

        pf = PrometheusForecast(registry)
        pf.exportAwsForecast()
        pf.exportGDSForecast()

        metric = prometheus_client.exposition.generate_latest(registry)
        return HttpResponse(metric, content_type=prometheus_client.exposition.CONTENT_TYPE_LATEST)
