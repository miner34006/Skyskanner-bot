# coding: utf-8

"""
Created on 29.07.2018

:author: Polianok Bogdan
"""

import json

import requests

from core.RequestData import RequestData, Leg
from core.skyskannerClasses.Itinerary import Itinerary
from parsers.ProxyParser import ProxyParser
from parsers.UserAgentParser import UserAgentParser
from core.utils.utils import findLegs


class SkyScanner:
    baseUrl = 'https://www.skyscanner.ru/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability'

    def __init__(self):
        self._userAgents = UserAgentParser()
        self._proxies = ProxyParser()

    def _sendRequest(self, trip, useProxy=False):
        """
        send request and get the data with all flights

        :param trip: object containing data for request
        :param useProxy: flag to use proxy
        :return: response from server
        :rtype: requests.response
        """
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

    def getItineraries(self, trip, useProxy=False):
        """
        make request, parse it and get list with Itineraries

        :param trip: object containing data for request
        :param useProxy: flag to use proxy
        :return: list with Itinerary objects
        :rtype: list
        """
        jsonResponse = json.loads(self._sendRequest(trip, useProxy).text)

        itineraries = []
        for itinerary in jsonResponse['itineraries']:
            for option in itinerary['pricing_options']:
                if 'amount' not in option['price'].keys():
                    continue

                legs = findLegs(jsonResponse, itinerary['leg_ids'][0])
                itineraries.append(Itinerary(itinerary, legs))

        return itineraries

    def scan(self, filters=[], *args, **kwargs):
        """
        scan the itineraries

        :param filters: filters applied to result
        :param args: non-keyworded params
        :param kwargs: keyworded params
        :return: list with itineraries
        :rtype: list
        """
        while True:
            itineraries = self.getItineraries(*args, **kwargs)
            for filter in filters:
                itineraries = filter(itineraries)

            yield itineraries


if __name__ == '__main__':
    from core.filters import filter_onlyCheapest, filter_onlyDirect

    scanner = SkyScanner()
    trip = RequestData([Leg(origin='VVO', destination='MOSC', date='2018-08-01')])

    filters = [filter_onlyDirect]
    for itineraries in scanner.scan(filters, trip=trip):
        print(itineraries)
