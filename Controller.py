# coding: utf-8

"""
Created on 11.01.2019

:author: Polianok Bogdan
"""

import requests
import logging

from vkApi.LongPoll import LongPoll, ADD_MESSAGE

logger = logging.getLogger(__name__)


class Controller:
    """
    Controller class. Send requests to Bot service.
    """
    def __init__(self):
        self.longPoll = LongPoll('169714719')
        self.cookies = {}

    def _getEvents(self):
        """
        Function to get events from longPoll

        :return: list with vk events
        :rtype: list
        """
        return next(self.longPoll.getEvents())

    def _getCookie(self, userId):
        """
        Get user-related cookie

        :param userId: vk user Id
        :type userId: str
        :return: user-related cookie
        :rtype: requests.cookies.RequestsCookieJar
        """
        if userId not in self.cookies:
            self.cookies[userId] = requests.cookies.RequestsCookieJar()

        return self.cookies[userId]

    def _setCookie(self, userId, cookie):
        """
        Set user-related cookie

        :param userId: vk user Id
        :type userId: str
        :param cookie: cookie to set
        :type cookie: requests.cookies.RequestsCookieJar
        :return: None
        """
        if cookie:
            self.cookies[userId] = cookie

    def start(self):
        """
        Function handles events from longPoll server and send requests to bot
        service

        :return: None
        """
        logger.info('Strating controller')
        while True:
            for event in self._getEvents():
                if event[0] == ADD_MESSAGE:
                    outbox = event[2] >> 1 & 1
                    if not outbox:
                        userId = event[3]
                        message = event[5]

                        logger.info('Revieve "{0}" message from user, notify botService'.format(message))
                        response = requests.post(
                            'http://localhost:5000/receive',
                            json={'userId': userId, 'message': message},
                            cookies=self._getCookie(userId)
                        )
                        self._setCookie(userId, response.cookies)


if __name__ == '__main__':
    logging.basicConfig(
        filename='./logs/controller.log',
        format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    controller = Controller()
    controller.start()
