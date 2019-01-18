import json
import logging

import requests
from flask import request, session, Response

from botService.vkBot import app
from botService.vkBot.UserSession import UserSession, SessionEncoder, asSession
from vkApi.api import apiRequest

logger = logging.getLogger(__name__)


@app.route('/send', methods=['POST'])
def sendMessage():
    """
    Api endpoint to send message from bot to user

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
    except requests.RequestException as e:
        logger.error(e)
        return Response(status=500)
    except KeyError as e:
        logger.error(e)
        return Response(status=400)


@app.route('/receive', methods=['POST'])
def receiveMessage():
    """
    Api endpoint to handle new message from user.

    :return: api response with status code
    :rtype: Response
    """
    try:
        data = request.get_json()
        userSession = UserSession(data['userId']) if str(data['userId']) not in session \
            else json.loads(session[str(data['userId'])], object_hook=asSession)

        logger.info('Got "{0}" action'.format(data['message']))
        userSession.execute(data['message'])
        session[str(data['userId'])] = str(json.dumps(userSession, cls=SessionEncoder))

        payload = {
            'user_id': data['userId'],
            'message': userSession.getInstruction(),
            'keyboard': json.dumps(userSession.getKeyboard(), ensure_ascii=False).encode("utf-8")
        }
        logger.info('Sending instructions to user')
        apiRequest('messages.send', payload)
        return Response(status=200)
    except requests.RequestException as e:
        logger.error(e)
        return Response(status=500)
    except KeyError as e:
        logger.error(e)
        return Response(status=400)
