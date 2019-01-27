# coding: utf-8

"""
Created on 12.01.2018

:author: Polianok Bogdan
"""

import sys
import os
import logging

import requests

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from modules.api import apiRequest

logger = logging.getLogger(__name__)
ADD_MESSAGE = 4


class LongPoll:
    """
    Class represented longPoll connection with VK server
    """

    def __init__(self, group_id):
        """"""
        self.group_id = group_id
        self._setUpLongPoll()

    def _setUpLongPoll(self):
        """
        Function to set up all connection variables for longPoll server work

        :return: None
        """
        logger.info('Establishing connection with a longPoll server')
        response = self._getSessionData(self.group_id)
        self._createConnectionVariables(
            server=response['server'],
            key=response['key'],
            ts=response['ts']
        )
        logger.info('Connection established')

    def _getSessionData(self, group_id, need_pts='0', lp_version='3'):
        """
        Getting data from API to work with LongPoll

        :param group_id: id of vk group
        :param need_pts: 1 by default (to return pts field)
        :param lp_version: long Poll version
        :return: response with key, server, ts data
        :rtype: dict
        """
        payload = {
            'need_pts': need_pts,
            'group_id': group_id,
            'lp_version': lp_version,
        }
        return apiRequest('messages.getLongPollServer', payload)['response']

    def _createConnectionVariables(self, server, key, ts, act='a_check',
                                   wait='25', mode='2', version='3'):
        """
        Initialize variables for LongPoll class

        :param server: server address
        :param key: secret key of session
        :param ts: number of last event
        :param act: a_check always
        :param wait: time to wait
        :param mode: additional response options
        :param version: version of API
        :return: None
        """
        self.longPollBaseUrl = 'https://{server}'.format(server=server)
        self.longPollPayload = {
            'act': act,
            'key': key,
            'ts': ts,
            'wait': wait,
            'mode': mode,
            'version': version,
        }

    def _updateTs(self, newTs):
        """
        Update longPollPayload with new TS

        :param newTs: new Ts
        :return: None
        """
        self.longPollPayload.update({'ts': newTs})

    def getEvents(self):
        """
        Expression generator. Get events from VK longPoll server

        :return: events from VK longPoll
        :rtype: list
        """
        while True:
            response = requests.get(self.longPollBaseUrl, self.longPollPayload)
            logger.debug('Get response from longPoll - {0}'.format(response.json()))

            if 'ts' not in response.json():
                self._setUpLongPoll()
                continue

            self._updateTs(response.json()['ts'])
            yield response.json()['updates']
