from django.urls import path
from report.views import PrometheusForecastView

urlpatterns = [
   path('forecast/',PrometheusForecastView.as_view(),name='prometheus_forecast') #if you update this, please do update url in report/processor.py function expoertMetric()
]
