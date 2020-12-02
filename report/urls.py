from django.urls import path
from report.views import PrometheusForecastView

urlpatterns = [
   path('metrics/',PrometheusForecastView.as_view(),name='prometheus_forecast')
]
