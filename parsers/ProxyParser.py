# coding: utf-8

"""
Created on 07.07.2018

:author: Polianok Bogdan
"""


class Proxy:
    def __init__(self, ipAdress, port, anonymity, https):
        self.ipAdress = ipAdress
        self.port = port
        self.anonymity = anonymity
        self.https = https


class ProxyParser:

    def __init__(self):
        self.__hasProxies = False
        self.__proxies = []

    def getRandomProxy(self):
        pass

    def getProxies(self):
        pass

    def updateProxies(self):
        pass