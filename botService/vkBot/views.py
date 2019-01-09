from flask import request
from flask import Response

from botService.vkBot import app
from vkApi.api import apiRequest


@app.route('/send', methods=['POST'])
def sendMessage():
    data = request.get_json()
    if 'userId' not in data or 'message' not in data:
        return Response(status=400)

    payload = {
        'user_id': data['userId'],
        'message': data['message'],
    }
    apiRequest('messages.send', payload)
    return Response(status=200)