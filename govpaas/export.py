import datetime as dt

from .models import BillingData
from report.helper.gecko import cleint as gecko_client


def export_to_gekkoboard(widget_uuid):
    today = dt.date.today()

    forecast_data = []

    billing_data = BillingData.objects.filter(year=today.year, month=today.month)

    for item in billing_data:

        space = item.space or "all spaces"
        text = f"{item.org}/{space}"

        forecast_data.append({
            'name': text,
            'forecast': float(format(item.forecast, '.2f')),
            'percent_diff': 0.0 if not item.percentage_change else float(format(item.percentage_change, '.2f'))
        })

    sorted_data = sorted(forecast_data, key=lambda el: el["forecast"], reverse=True)

    payload = gecko_client().leaderboard_format(data=sorted_data)
    gecko_client().push(widget_uuid=widget_uuid, payload=payload)
