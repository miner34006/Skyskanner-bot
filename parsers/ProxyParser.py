# coding: utf-8

"""
Created on 07.07.2018

:author: Polianok Bogdan
"""

import random
import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup


from parsers.Proxy import Proxy


class ProxyParser:
    """
    Class that parses the website (https://free-proxy-list.net) and
    gets actual proxies (random proxy or list of it).

     """

    def __init__(self):
        self._hasProxies = False
        self._proxies = []

    def getRandomProxy(self):
        """
        Select random Proxy from self._proxies

        :return: Proxy
        """
        if not self._hasProxies:
            self._createProxies()
        return random.choice(self._proxies)

    def getRandomHttpsProxy(self):
        """
        select and return random https proxy from self._proxies

        :return: random https proxy
        """
        if not self._hasProxies:
            self._createProxies()
        return random.choice([proxy for proxy in self._proxies if proxy.https])

    def getRandomHttpProxy(self):
        """
        select and return random http proxy from self._proxies

        :return: random http proxy
        """
        if not self._hasProxies:
            self._createProxies()
        return random.choice([proxy for proxy in self._proxies if not proxy.https])

    def getProxies(self):
        """
        Getting self._proxies

        :return: list of Proxy
        """
        if not self._hasProxies:
            self._createProxies()
        return self._proxies

    def updateProxies(self):
        """
        Updates self._proxies

         :return: None
         """
        self._clearProxies()
        self._createProxies()

    def _createProxies(self):
        """
        Creates self._proxies and changes _hasProxies flag

        :return: None
        """
        self._proxies = self._parseProxies()
        self._hasProxies = True

    def _clearProxies(self):
        """
        Clears self._proxies and changes _hasProxies flag

         :return: None
         """
        self._proxies = []
        self._hasProxies = False

    def _checkProxy(self, proxy):
        """
        checks proxy functionality

        :param proxy: proxy needed to check
        :return: proxy if working, None instead
        """
        proxies = {}
        if proxy.https:
            proxies.update({'https': str(proxy)})
        else:
            proxies.update({'http': str(proxy)})

        url = 'https://www.google.ru'
        try:
            requests.get(url, proxies=proxies, timeout=3)
        except requests.exceptions.RequestException as e:
            return None
        else:
            return proxy

    def _parseProxies(self):
        """
        Parses the website and finds actual proxies

         :return: list of Proxies
         """
        url = 'https://free-proxy-list.net/'
        response = requests.get(url).content
        soup = BeautifulSoup(response, "html.parser")

        proxyListTable = soup.find('table', attrs={'id': 'proxylisttable'})
        proxies = proxyListTable.find_all('tr')
        proxies = proxies[1: len(proxies) - 1]

        proxyList = []
        for proxy in proxies:
            proxyData = proxy.find_all('td')

            ipAddress = proxyData[0].string
            port = proxyData[1].string
            https = proxyData[6].string

            proxy = Proxy(ipAddress, port, https)
            proxyList.append(proxy)

        pool = Pool(20)
        activeProxies = pool.map(self._checkProxy, proxyList)

        return [proxy for proxy in activeProxies if proxy is not None]

