import time
import json
import threading

import requests
from flask import request, Response

from searchService.searchingEngine import app
from searchService.core.filters import filter_onlyCheapest, filter_onlyDirect
from searchService.core.RequestData import RequestData
from searchService.core.Skyskanner import SkyScanner
from searchService.parsers.ProxyParser import ProxyParser
from searchService.parsers.UserAgentParser import UserAgentParser
from searchService.searchingEngine.constants import cities
from vkApi.api import apiRequest

searchingTasks = {}

class Searcher(threading.Thread):
    def __init__(self, sourceCity, targetCity, price, date, userId):
        super().__init__()
        self.sourceCity = sourceCity
        self.targetCity = targetCity
        self.price = int(price)
        self.date = date
        self.userId = userId
        self.stopThread = False
        self.scanner = SkyScanner(UserAgentParser(), ProxyParser())

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
            print(tries)
            tries += 1

    def stop(self):
        self.stopThread = True


def stopExistingTask(userId):
    global searchingTasks
    if userId in searchingTasks and searchingTasks[userId]:
        searchingTasks[userId].stop()
        searchingTasks[userId] = None

def startSearchingTask(data):
    stopExistingTask(int(data['userId']))
    global searchingTasks
    searchingTasks[int(data['userId'])] = Searcher(data['sourceCity'], data['targetCity'], data['price'], data['date'], int(data['userId']))
    searchingTasks[int(data['userId'])].start()

@app.route('/start-search', methods=['POST'])
def startSearch():
    data = request.get_json()
    try:
        startSearchingTask(data)
        return Response(status=200)
    except KeyError as _:
        return Response(status=400)


@app.route('/stop-search', methods=['POST'])
def stopSearch():
    data = request.get_json()
    try:
        stopExistingTask(int(data['userId']))
        return Response(status=200)
    except KeyError as _:
        return Response(status=400)


@app.route('/is-searching', methods=['POST'])
def isSearching():
    data = request.get_json()
    try:
        global searchingTasks
        returnData = {
            'isSearching': True if searchingTasks[int(data['userId'])] else False,
            'searchingQuery': {
                'sourceCity': searchingTasks[int(data['userId'])].sourceCity,
                'targetCity': searchingTasks[int(data['userId'])].targetCity,
                'date': searchingTasks[int(data['userId'])].date
            } if searchingTasks[int(data['userId'])] else None
        }
        return Response(json.dumps(returnData), status=200, mimetype='application/json')
    except KeyError as _:
        return Response(status=400)
