from calendar import monthrange
from collections import defaultdict
import datetime as dt
from dateutil.relativedelta import *
from decimal import Decimal
import json

from django.conf import settings
import requests

from .client import Client
from .models import BillingData, Space


def _days_in_month(date):
    return monthrange(date.year, date.month)[1]


def build_query_date_ranges():
    """build the start/end date ranges for current month and previous month.
    The previous month is from 1 - last day of month; the current date is from 1 to current day
    """
    current_date = dt.date.today()

    prev_month = current_date - relativedelta(months=1)
    days_in_month = _days_in_month(prev_month)

    last_month_range = (prev_month+relativedelta(day=1), prev_month+relativedelta(day=days_in_month))
    curr_month_range = (current_date+relativedelta(day=1), current_date,)

    return last_month_range, curr_month_range


def get_per_space_billing_data(client, org_guid, start_date, end_date):
    """Take the raw per service data and calculate per space amount"""

    cost_data = defaultdict(lambda: 0)

    data = client.get_billing_data(org_guid, str(start_date), str(end_date))

    for row in data:
        if "price" in row:
            # legacy API format
            cost_data[row["space_name"]] += float(row["price"]["ex_vat"])
        else:
            # New API format
            cost_data[row["space_name"]] += row["charge_gbp_exc_vat"]

    return dict(cost_data)


def generate_forecast(current_amount, last_month_amount, current_date):
    """Forecast this months bill and calculate the percentage change from last month, based on that forecast"""

    percentage_change = None

    forecast = Decimal(current_amount / current_date.day * _days_in_month(current_date))

    if last_month_amount:
        percentage_change = (forecast - last_month_amount) / last_month_amount * 100

    return forecast, percentage_change


def import_billing_data():
    """ Main entryppoint. Gets the current billing data for each org, forecasts the month's bill and the percentage change from last month."""

    client = Client(settings.GDS_PAAS_API_URL, settings.GDS_BILLING_API_URL, settings.GDS_USER, settings.GDS_USER_PASS)
    orgs = client.get_orgs()

    last_month_range, curr_month_range = build_query_date_ranges()
    last_month = last_month_range[0]

    for org in orgs:
        # complete=True indicates that we have a full month's data.
        have_prev_month_data = BillingData.objects.filter(org=org["name"], month=last_month.month, year=last_month.year, complete=True).exists()

        if not have_prev_month_data:
            # get last month's billing data so we can calculate %change; note % change is only required for gekkoboard
            prev_month_data = get_per_space_billing_data(client, org["guid"], *last_month_range)

            default_fields = {
                "year": last_month.year,
                "month": last_month.month,
                "org": org["name"],
            }

            for space, amount in prev_month_data.items():
                BillingData.objects.create(
                    space=space,
                    defaults={
                        "amount": amount,
                        "complete": True,
                    }
                    **default_fields,
                )

            # add org total - the org total has no space set, e.g. space=""
            BillingData.objects.update_or_create(
                space="",
                defaults={
                    "amount": sum(prev_month_data.values()),
                    "complete": True,
                }
                **default_fields,
            )

        # get this month's data - from the 1st of the month to the current day of the month
        # then calculate the forecast (avg spent per day currently * number of days in month),
        # and the percentage change with the previous month.
        # set complete=False because we don't have the full month's data yet.
        curr_month_data = get_per_space_billing_data(client, org["guid"], *curr_month_range)

        # TODO: should we include today in the billing query date range, as today is not complete?
        # the API endpoint will forecast, e.g it will estimate the cost until end of the day. BUT this will mean
        # the current amount is potentially slightly inaccurate.

        default_fields = {
            "year": curr_month_range[1].year,
            "month": curr_month_range[1].month,
            "org": org["name"],
            "complete": False,
        }

        prev_month_data = {
            obj.space: obj.amount for obj in
            BillingData.objects.filter(org=org["name"], month=last_month.month, year=last_month.year, complete=True)
        }

        for space, amount in curr_month_data.items():

            forecast, percentage_change = generate_forecast(amount, prev_month_data.get(space, None), curr_month_range[1])

            BillingData.objects.update_or_create(
                space=space,
                defaults={
                    "amount": amount,
                    "forecast": forecast,
                    "percentage_change": percentage_change,
                },
                **default_fields,
            )

        # Add org total
        org_amount = sum(curr_month_data.values())
        forecast, percentage_change = generate_forecast(org_amount, prev_month_data.get("", None), curr_month_range[1])

        BillingData.objects.update_or_create(
            space="",
            defaults={
                "amount": org_amount,
                "forecast": forecast,
                "percentage_change": percentage_change,
            },
            **default_fields,
        )
