# -*- coding: utf-8 -*-

"""
:author: Polianok Bogdan
"""

import sys
import logging
import requests


BASE_URL = "https://api.vk.com/method/"
GROUP_TOKEN = 'e30b7d7b16eb6ad8420986e7fd086bedd630e91b3612e0895ff18a2cd6934fc77a3552eec87d747e1adbb'
V = '5.80'

logger = logging.getLogger(__name__)


def apiRequest(method, payload=None):
    """
    Get request from vk server

    :param get: method for vkApi
    :param payload: parameters for vkApi

    :return: answer from vkApi
    """

    if payload is None:
        payload = {}

    if not ('access_token' in payload):
        payload.update({'access_token': GROUP_TOKEN, 'v': V})

    try:
        response = requests.post(BASE_URL + method, payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(e)
        sys.exit(1)
