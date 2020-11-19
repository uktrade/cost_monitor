from django.views import View
from django.http import HttpResponse
from report.helper.export.prometheus import PrometheusForecast

class PrometheusForecastView(View):
    pf = PrometheusForecast()
    def get(self,request):   
        self.pf.exportAwsForecast()
        self.pf.exportGDSForecast()
        return HttpResponse('OK')
