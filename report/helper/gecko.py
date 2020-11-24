
import json
import requests
from django.conf import settings


class cleint:

    def __init__(self):
        self.webClient = requests.session()

    def push(self, widget_uuid, payload):
        requests.post(
            "https://push.geckoboard.com/v1/send/{}".format(widget_uuid), data=payload)

    def leaderboard_format(self, data):
        formated_board = list()
        widget_data = dict()
        for info in data:
            colour = 'green'
            if info['percent_diff'] > 0:
                colour = 'red'

            formated_board.append({'title': {'text': ''}, 'label': {'name': info['name'], 'color': colour},
                                   "description": "Forecast: {} Change: {}%".format(info['forecast'], info['percent_diff'])})

        widget_data = {'api_key': settings.GECKO_TOKEN, 'data': formated_board}
        return json.dumps(widget_data)
