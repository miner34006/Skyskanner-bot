# coding: utf-8

"""
Created on 29.07.2018

:author: Polianok Bogdan
"""


import json
import time

import requests

from core.RequestData import RequestData, Leg
from core.skyskannerClasses.Itinerary import Itinerary
from core.utils.decorators import deprecated
from parsers.ProxyParser import ProxyParser
from parsers.UserAgentParser import UserAgentParser


class SkyScanner:
    baseUrl = 'https://www.skyscanner.ru/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query'

    def __init__(self):
        self._userAgents = UserAgentParser()
        self._proxies = ProxyParser()
        self._userAgents.updateUserAgents()
        self._proxies.updateProxies()

    def _sendRequest(self, trip, useProxy=False):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Skyscanner-ChannelId': 'website',
            'User-Agent': self._userAgents.getRandomUserAgent(),
        }

        proxies = {}
        if useProxy:
            proxies = {'http': str(self._proxies.getRandomHttpProxy()), 'https': str(self._proxies.getRandomHttpsProxy())}

        response = requests.post(self.baseUrl,
                                 data=trip.getJsonRepresentation(),
                                 headers=headers,
                                 proxies=proxies,
                                 timeout=5)

        if response.status_code == 200:
            return response
        else:
            raise requests.exceptions.HTTPError(response.text)



    #TODO
    @deprecated
    def getDirectTickets(self, trip):
        jsonResponse = json.loads(self._sendRequest(trip).text)
        directLegs = [leg for leg in jsonResponse['legs'] if leg['stop_count'] == 0]

        itineraries = []
        for itinerary in jsonResponse['itineraries']:
            for leg in directLegs:
                if leg['id'] in itinerary['leg_ids']:
                    itineraries.append(Itinerary(itinerary))

        return itineraries

    #TODO
    @deprecated
    def getTickets(self, trip, bottomPrice, topPrice, isDirect=False, count=5):
        jsonResponse = json.loads(self._sendRequest(trip).text)

        tickets = []
        for itinerary in jsonResponse['itineraries']:
            for option in itinerary['pricing_options']:
                if 'amount' not in option['price'].keys():
                    continue

                if bottomPrice < option['price']['amount'] < topPrice:
                    tickets.append(itinerary)

        return tickets

    def getCheapestTicket(self, trip, useProxy=False):
        jsonResponse = json.loads(self._sendRequest(trip, useProxy).text)

        cheapestTicket = {'ticket': None, 'amount': None}
        for itinerary in jsonResponse['itineraries']:
            for option in itinerary['pricing_options']:
                if 'amount' not in option['price'].keys():
                    continue

                if (cheapestTicket['ticket'] is None) or (option['price']['amount'] < cheapestTicket['amount']):
                    cheapestTicket['ticket'] = itinerary
                    cheapestTicket['amount'] = option['price']['amount']

        return Itinerary(cheapestTicket['ticket'])

if __name__ == '__main__':
    scanner = SkyScanner()
    trip = RequestData([Leg(origin='MOSC', destination='VVO', date='2018-08-01')])

    for _ in range(1000):
        try:
            minPrice = scanner.getCheapestTicket(trip, useProxy=True).getMinPrice()
            print(minPrice)
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(3)

