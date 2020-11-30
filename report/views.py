from django.views import View
from django.http import HttpResponse
from report.helper.export.prometheus import PrometheusForecast
import prometheus_client
class PrometheusForecastView(View):

    def get(self,request):
        pf = PrometheusForecast()
        registry = pf.getRegistry()
        pf.exportAwsForecast()
        pf.exportGDSForecast()
        metric = prometheus_client.exposition.generate_latest(registry)
        return HttpResponse(metric,content_type=prometheus_client.exposition.CONTENT_TYPE_LATEST)
