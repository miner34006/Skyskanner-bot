import requests
import time
import threading

from searchService.core.filters import filter_onlyCheapest, filter_onlyDirect
from searchService.core.RequestData import RequestData
from searchService.core.Skyskanner import SkyScanner
from searchService.searchingEngine.constants import cities
from vkApi.api import apiRequest


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
