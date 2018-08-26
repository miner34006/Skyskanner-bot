# coding: utf-8

"""
Created on 07.07.2018

:author: Polianok Bogdan
"""

import random
import sys
from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool


class UserAgentParser:
    """
    Class that parses the website (https://developers.whatismybrowser.com) and
    gets actual user agents (random user agent or list of it).
    """

    SOFTWARE = {
        'internetExplorer': 'https://developers.whatismybrowser.com/useragents/explore/software_name/internet-explorer/',
        'androidBrowser': 'https://developers.whatismybrowser.com/useragents/explore/software_name/android-browser/',
        'firefox': 'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/',
        'opera': 'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
        'safari': 'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
    }

    def __init__(self):
        self._hasUserAgents = False
        self._userAgents = []

    def getRandomUserAgent(self):
        """
        Select random user agent from self.__userAgents

        :return: random user agent
        """
        if not self._hasUserAgents:
            self._createUserAgents()
        return random.choice(self._userAgents)

    def getUserAgents(self):
        """
        Getting self.__userAgents

        :return: user agents list
        """
        if not self._hasUserAgents:
            self._createUserAgents()
        return self._userAgents

    def updateUserAgents(self):
        """
        Updates self.__userAgents

        :return: None
        """
        self._clearUserAgents()
        self._createUserAgents()

    def _createUserAgents(self):
        """
        Creates self.__userAgents and changes __hasUserAgents flag

        :return: None
        """
        pool = Pool(5)

        try:
            results = pool.map(self._parseUserAgents, self.SOFTWARE.values())
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        finally:
            pool.close()
            pool.join()

        for element in results:
            self._appendToUserAgents(element)
        self._hasUserAgents = True

    def _clearUserAgents(self):
        """
        Clears self.__userAgents and changes __hasUserAgents flag

        :return: None
        """
        self._userAgents = []
        self._hasUserAgents = False

    def _parseUserAgents(self, software):
        """
        Parses the website and finds associated user agents with the software

        :param software: link to software
        :return: list of user agents
        """
        if software not in self.SOFTWARE.values():
            raise ValueError('Invalid function parameter')

        response = requests.get(software)
        soup = BeautifulSoup(response.content, "html.parser")
        userAgents = soup.find_all('td', class_='useragent')
        return [userAgent.string for userAgent in userAgents]

    def _appendToUserAgents(self, userAgents):
        """
        Append elements of user agents list to self.__userAgents

        :param userAgents: list of user agents needed to append
        :return: None
        """
        for userAgent in userAgents:
            self._userAgents.append(userAgent)

