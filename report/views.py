from django.views import View
from django.http import HttpResponse
from report.helper.export.prometheus import Prometheus,PrometheusForecast


class PrometheusView(View):
    p = Prometheus()
    def get(self,request):
        self.p.exportAwsCost()
        self.p.exportGDSCost()
        self.p.exportHerokuCost()
        return HttpResponse('OK')

class PrometheusForecastView(View):
    pf = PrometheusForecast()
    def get(self,request):   
        self.pf.exportAwsForecast()
        self.pf.exportGDSForecast()
        self.pf.exportHerokuForecast()
        return HttpResponse('OK')
