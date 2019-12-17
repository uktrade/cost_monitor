from django.views import View
from report.helper.export.prometheus import Prometheus,PrometheusForecast


class PrometheusView(View):
    p = Prometheus()
    p.exportAws()
    p.exportGDS()
    p.exportHeroku()

class PrometheusForecastView(View):
    pf = PrometheusForecast()
    #pf.exportAwsForecast()
    pf.exportGDSForecast()
    # pf.exportHerokuForecast()
