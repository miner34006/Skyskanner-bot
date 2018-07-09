# coding: utf-8

"""
Created on 07.07.2018

:author: Polianok Bogdan
"""

import random
import requests
from bs4 import BeautifulSoup

from parsers.Proxy import Proxy


class ProxyParser:

    PROXY_WEBSITE = 'https://free-proxy-list.net'

    def __init__(self):
        self.__hasProxies = False
        self.__proxies = []

    def getRandomProxy(self):
        if not self.__hasProxies:
            self.__createProxies()
        return random.choice(self.__proxies)

    def getProxies(self):
        if not self.__hasProxies:
            self.__createProxies()
        return self.__proxies

    def updateProxies(self):
        self.__clearProxies()
        self.__createProxies()

    def __createProxies(self):
        self.__proxies = self.__parseProxies()
        self.__hasProxies = True

    def __clearProxies(self):
        self.__proxies = []
        self.__hasProxies = False

    def __parseProxies(self):
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

        return proxyList
