from django.urls import path

from report.views import PrometheusView,PrometheusForecastView

urlpatterns = [
    path('costMetric/',PrometheusView.as_view(),name='prometheus_cost'),
    path('forecastMetric/',PrometheusForecastView.as_view(),name='prometheus_forecast')
]