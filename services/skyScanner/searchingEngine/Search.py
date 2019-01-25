import requests
import time
import threading
import sys
import os

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from skyScanner.core.filters import filter_onlyCheapest, filter_onlyDirect
from skyScanner.core.RequestData import RequestData
from skyScanner.core.Skyskanner import SkyScanner
from skyScanner.searchingEngine.constants import cities
from modules.api import apiRequest


class Search(threading.Thread):
    def __init__(self, searchData, userToNotify, userAgentParser=None, proxyParser=None):
        super().__init__()

        self.sourceCity = searchData['sourceCity']
        self.targetCity = searchData['targetCity']
        self.date = searchData['date']
        self.price = int(searchData['price'])

        self.userId = userToNotify
        self.stopThread = False
        self.scanner = SkyScanner(userAgentParser, proxyParser)

    def run(self):
        tries = 0
        price = self.price
        global searchingTasks
        filters = [filter_onlyDirect]
        trip = RequestData([{
            'origin': cities[self.sourceCity],
            'destination': cities[self.targetCity],
            'date': self.date
        }])

        for itineraries in self.scanner.scan(filters, trip=trip, useProxy=True):
            try:
                cheapestOption = itineraries[0].getCheapestPriceOptions()[0]
            except Exception as _:
                continue

            response = apiRequest('utils.getShortLink', {'url': cheapestOption.getLinkForBuying()})
            if int(cheapestOption) < price or (tries == 30 and int(cheapestOption) < self.price):
                price = int(cheapestOption)
                message = 'Pricing option: {option};\n\n Link: {link}'.format(
                    option=cheapestOption,
                    link=response['response']['short_url']
                )
                requests.post('http://localhost:5000/send', json={'userId': self.userId, 'message': message})
                tries = 0

            if self.stopThread:
                break

            time.sleep(10)
            tries += 1

    def stop(self):
        self.stopThread = True
