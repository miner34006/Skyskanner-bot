import json
import sys
import os

from flask import request, Response

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from skyScanner.searchingEngine import app
from skyScanner.parsers.ProxyParser import ProxyParser
from skyScanner.parsers.UserAgentParser import UserAgentParser
from skyScanner.searchingEngine.Search import Search

userAgentParser = UserAgentParser()
proxyParser = ProxyParser()

searchingTasks = {}


@app.route('/search/<int:searchId>', methods=['GET'])
def getSearch(searchId):
    try:
        search = {
            'sourceCity': searchingTasks[searchId].sourceCity,
            'targetCity': searchingTasks[searchId].targetCity,
            'date': searchingTasks[searchId].date
        }
        return Response(json.dumps(search), status=200, mimetype='application/json')
    except KeyError:
        return Response(status=404)

@app.route('/search', methods=['GET'])
def getSearches():
    searches = []
    for searchId in searchingTasks:
        returnData.append({
            'searchId': searchId,
            'sourceCity': searchingTasks[searchId].sourceCity,
            'targetCity': searchingTasks[searchId].targetCity,
            'date': searchingTasks[searchId].date
        })
    return Response(json.dumps(searches), status=200, mimetype='application/json')

@app.route('/search/<int:searchId>', methods=['DELETE'])
def deleteSearch(searchId):
    global searchingTasks
    try:
        searchingTasks[searchId].stop()
        searchingTasks.pop(searchId)
        return Response(status=204)
    except KeyError:
        return Response(status=404)

@app.route('/search', methods=['DELETE'])
def deleteSearches():
    global searchingTasks
    for searchId in searchingTasks:
        searchingTasks[searchId].stop()
        searchingTasks.pop(searchId)
    return Response(status=204)

@app.route('/search', methods=['POST'])
def createSearch():
    global searchingTasks
    data = request.get_json()
    try:
        searchingTasks[int(data['userId'])] = Search(
            searchData=data,
            userToNotify=data['userId'],
            userAgentParser=userAgentParser,
            proxyParser=proxyParser
        )
        searchingTasks[int(data['userId'])].start()
    except KeyError:
        return Response(status=400)
    return Response(status=201)
