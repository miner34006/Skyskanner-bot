import json

import requests
from flask import request, session, Response

from botService.vkBot import app
from botService.vkBot.UserSession import UserSession, SessionEncoder, asSession
from vkApi.api import apiRequest


@app.route('/send', methods=['POST'])
def sendMessage():
    """ api endpoint to send message from bot to user

    :return: api response with status code
    :rtype: Response
    """
    data = request.get_json()
    try:
        payload = {
            'user_id': data['userId'],
            'message': data['message'],
        }
        apiRequest('messages.send', payload)
        return Response(status=200)
    except requests.RequestException as _:
        return Response(status=500)
    except KeyError as _:
        return Response(status=400)


@app.route('/receive', methods=['POST'])
def receiveMessage():
    """ api endpoint to handle new message from user

    :return: api response with status code
    :rtype: Response
    """
    data = request.get_json()
    userSession = UserSession() if str(data['userId']) not in session \
        else json.loads(session[str(data['userId'])], object_hook=asSession)

    userSession.execute(data['message'])
    session[str(data['userId'])] = str(json.dumps(userSession, cls=SessionEncoder))

    try:
        payload = {
            'user_id': data['userId'],
            'message': userSession.getInstruction(),
            'keyboard': json.dumps(userSession.getKeyboard(), ensure_ascii=False).encode("utf-8")
        }
        apiRequest('messages.send', payload)
        return Response(status=200)
    except requests.RequestException as _:
        return Response(status=500)
    except KeyError as _:
        return Response(status=400)
