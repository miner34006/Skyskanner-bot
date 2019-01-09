# coding: utf-8

"""
Created on **.**.2018

:author: Polianok Bogdan
"""

import json

from vkApi.LongPoll import LongPoll
from vkApi.UserSession import UserSession
from parsers.ProxyParser import ProxyParser
from parsers.UserAgentParser import UserAgentParser
from vkApi.api import apiRequest
from vkApi.constants import ADD_MESSAGE
from core.Skyskanner import SkyScanner


class VkBot:
    def __init__(self):
        self.longPoll = LongPoll('169714719')
        self.sessions = []

        self._userAgents = UserAgentParser()
        self._userAgents.updateUserAgents()

        self._proxies = ProxyParser()
        self._proxies.updateProxies()

        self.scanner = SkyScanner(self._userAgents, self._proxies)

    def _getEvents(self):
        return next(self.longPoll.getEvents())

    def _getUserSession(self, userId):
        for userSession in self.sessions:
            if userSession.userId == userId:
                return userSession

    def _sendResponse(self, userId):
        payload = {
            'user_id': userId,
            'message': self._getUserSession(userId).getInstruction(),
        }
        if self._getUserSession(userId).getKeyboard() is not None:
            payload.update(
                {'keyboard': json.dumps(self._getUserSession(userId).getKeyboard(), ensure_ascii=False).encode("utf-8")}
            )
        apiRequest('messages.send', payload)

    def start(self):
        while True:
            for event in self._getEvents():
                if event[0] == ADD_MESSAGE:
                    outbox = event[2] >> 1 & 1
                    if not outbox:
                        userId = event[3]
                        message = "message"

                        import requests
                        requests.post('http://localhost:5000/send', json={'userId':userId, 'message':message})


                        # activeSessions = [userSession.userId for userSession in self.sessions]
                        # if userId not in activeSessions:
                        #     self.sessions.append(UserSession(userId, self.scanner))
                        #
                        # action = event[5]
                        # self._getUserSession(userId).execute(action)
                        # self._sendResponse(userId)


if __name__ == '__main__':
    bot = VkBot()
    bot.start()
