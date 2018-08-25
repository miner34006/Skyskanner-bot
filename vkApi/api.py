# -*- coding: utf-8 -*-

"""

:author: Polianok Bogdan

"""

import requests
import json

BASE_URL = "https://api.vk.com/method/"

GROUP_TOKEN = 'e30b7d7b16eb6ad8420986e7fd086bedd630e91b3612e0895ff18a2cd6934fc77a3552eec87d747e1adbb'

V = '5.80'


def apiRequest(method, payload=None):
    """Get request from vk server
      
    :param get: method for vkApi
    :param payload: parameters for vkApi
    
    :return: answer from vkApi
    
    """

    if payload is None:
        payload = {}

    if not ('access_token' in payload):
        payload.update({'access_token': GROUP_TOKEN, 'v': V})

    response = requests.get(BASE_URL + method, payload)
    data = json.loads(response.text)
    return data

