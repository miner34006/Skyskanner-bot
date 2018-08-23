# -*- coding: utf-8 -*-

"""

:author: Polianok Bogdan

"""

import requests
import json

from constants import Events

BASE_URL = "https://api.vk.com/method/"

GROUP_TOKEN = 'e30b7d7b16eb6ad8420986e7fd086bedd630e91b3612e0895ff18a2cd6934fc77a3552eec87d747e1adbb'

V = '5.80'


class LongPoll:
    def __init__(self, group_id):
        response = self._getSessionData(group_id)['response']
        self._createConnectionVariables(
            server=response['server'],
            key=response['key'],
            ts=response['ts']
        )

    def _getSessionData(self, group_id, need_pts='0', lp_version='3'):
        payload = {
            'need_pts': need_pts,
            'group_id': group_id,
            'lp_version': lp_version,
        }
        return apiRequest('messages.getLongPollServer', payload)

    def _createConnectionVariables(self, server, key, ts, act='a_check', wait='25', mode='2', version='3'):
        self.longPollBaseUrl = 'https://{server}'.format(server=server)
        self.longPollPayload = {
            'act': act,
            'key': key,
            'ts': ts,
            'wait': wait,
            'mode': mode,
            'version': version,
        }

    def _updateTs(self, newTs):
        self.longPollPayload.update(
            {'ts': newTs}
        )

    def createPipe(self):
        while True:
            response = requests.get(self.longPollBaseUrl, self.longPollPayload)
            jsonResponse = json.loads(response.text)
            self._updateTs(jsonResponse['ts'])
            yield jsonResponse['updates']


def apiRequest(method, payload=None):
    """Get request from vk server
      
    :param get: method for vkApi
    :param payload: parameters for vkApi
    
    :return: answer from vkApi
    
    """

    if payload is None:
        payload = {}

    if not ('access_token' in payload):
        payload.update({'access_token': GROUP_TOKEN, 'v': V})

    response = requests.get(BASE_URL + method, payload)
    data = json.loads(response.text)
    return data


if __name__ == '__main__':

    keyboard = {
        "one_time": False,
        "buttons": [[
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"3\"}",
                    'label': 'ПОЛУЧИТЬ ДЕШЕВЫЕ БИЛЕТЫ',
                },
                'color': 'primary'
            }
        ]]
    }

    from core.filters import filter_onlyCheapest, filter_onlyDirect
    from core.Skyskanner import SkyScanner
    from core.RequestData import RequestData

    scanner = SkyScanner()
    trip = RequestData([{'origin': 'VVO', 'destination': 'MOSC', 'date': '2018-08-30'}])
    filters = [filter_onlyCheapest]

    longPoll = LongPoll('169714719')
    for events in longPoll.createPipe():
        for event in events:
            if event[0] == Events.ADD_MESSAGE:
                outbox = event[2] >> 1 & 1
                if not outbox:
                    if (event[5] == 'ПОЛУЧИТЬ ДЕШЕВЫЕ БИЛЕТЫ'):
                        itineraries = scanner.scan(filters, trip=trip)
                        elem = str(next(itineraries)[0])
                        print(apiRequest('messages.send', {
                            'user_id': event[3],
                            'message': elem,
                            'keyboard': json.dumps(keyboard, ensure_ascii=False).encode("utf-8")
                        }))
