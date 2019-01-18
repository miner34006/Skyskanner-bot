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


def deleteSearch(searchId):
    def deleteEntity(entityId):
        global searchingTasks
        searchingTasks[int(entityId)].stop()
        searchingTasks.pop(int(entityId))

    if searchId:
        deleteEntity(searchId)
    else:
        for searchId in searchingTasks:
            deleteEntity(searchId)

def postSearch(data):
    try:
        deleteSearch(data['userId'])
    except:
        pass

    global searchingTasks
    searchingTasks[int(data['userId'])] = Searcher(data['sourceCity'], data['targetCity'], data['price'], data['date'], int(data['userId']))
    searchingTasks[int(data['userId'])].start()

def getSearch(searchId):
    if searchId:
        returnData = {
            'sourceCity': searchingTasks[searchId].sourceCity,
            'targetCity': searchingTasks[searchId].targetCity,
            'date': searchingTasks[searchId].date
        }
    else:
        returnData = []
        for searchId in searchingTasks:
            returnData.append({
                'searchId': searchId,
                'sourceCity': searchingTasks[searchId].sourceCity,
                'targetCity': searchingTasks[searchId].targetCity,
                'date': searchingTasks[searchId].date
            })
    return returnData


@app.route('/search', defaults={'searchId': None}, methods=['GET', 'POST', 'DELETE'])
@app.route('/search/<int:searchId>', methods=['GET', 'DELETE'])
def search(searchId):
    if request.method == 'GET':
        try:
            return Response(json.dumps(getSearch(searchId)), status=200, mimetype='application/json')
        except KeyError:
            return Response(status=404)

    elif request.method == 'POST':
        try:
            postSearch(request.get_json())
        except KeyError:
            return Response(status=500)
        return Response(status=201)

    elif request.method == 'DELETE':
        try:
            deleteSearch(searchId)
            return Response(status=204)
        except KeyError:
            return Response(status=404)

