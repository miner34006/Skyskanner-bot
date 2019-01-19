# coding: utf-8

"""
Created on 09.07.2018

:author: Polianok Bogdan
"""

import sys
import os
import unittest

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from parsers.ProxyParser import ProxyParser
from searchService.parsers.Proxy import Proxy


class ProxyParserTestCase(unittest.TestCase):
    def test_initialization(self):
        parser = ProxyParser()
        self.assertFalse(parser._hasProxies)
        self.assertListEqual([], parser._proxies)

    def test_clearProxies(self):
        parser = ProxyParser()
        parser.getProxies()
        parser._clearProxies()
        self.assertFalse(parser._hasProxies)
        self.assertListEqual([], parser._proxies)

    def test_getRandomProxy(self):
        parser = ProxyParser()
        randomChoice = parser.getRandomProxy()
        self.assertIn(randomChoice, parser._proxies)

    def test_getRandomProxyEvoke__createProxies(self):
        parser = ProxyParser()
        parser.getRandomProxy()
        self.assertTrue(parser._hasProxies)
        self.assertNotEqual([], parser._proxies)

    def test_getProxies(self):
        parser = ProxyParser()
        proxies = parser.getProxies()
        self.assertListEqual(proxies, parser._proxies)

    def test_getProxiesEvoke__createProxies(self):
        parser = ProxyParser()
        parser.getProxies()
        self.assertTrue(parser._hasProxies)
        self.assertNotEqual([], parser._proxies)

    def test_updateProxies(self):
        parser = ProxyParser()
        parser.updateProxies()
        self.assertTrue(parser._hasProxies)
        self.assertNotEqual([], parser._proxies)

    def test_createProxies(self):
        parser = ProxyParser()
        parser._createProxies()
        self.assertTrue(parser._hasProxies)
        self.assertNotEqual([], parser._proxies)

    def test_parseProxies(self):
        parser = ProxyParser()
        someList = parser._parseProxies()
        self.assertIsInstance(someList, list)
        self.assertNotEqual([], someList)

    def test_getRandomHttpsProxy(self):
        parser = ProxyParser()
        for _ in range(10):
            proxy = parser.getRandomHttpsProxy()
            self.assertIsInstance(proxy, Proxy)
            self.assertEqual(True, proxy.https)

    def test_getRandomHttpProxy(self):
        parser = ProxyParser()
        for _ in range(10):
            proxy = parser.getRandomHttpProxy()
            self.assertIsInstance(proxy, Proxy)
            self.assertEqual(False, proxy.https)


if __name__ == '__main__':
    unittest.main()

