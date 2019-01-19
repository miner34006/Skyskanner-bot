# coding: utf-8

"""
Created on 07.07.2018

:author: Polianok Bogdan
"""

import sys
import os
import unittest

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from searchService.parsers.UserAgentParser import UserAgentParser


class UserAgentParserTestCase(unittest.TestCase):
    def test_initialization(self):
        parser = UserAgentParser()
        self.assertFalse(parser._hasUserAgents)
        self.assertListEqual([], parser._userAgents)

    def test_clearUserAgents(self):
        parser = UserAgentParser()
        parser.getUserAgents()
        parser._clearUserAgents()
        self.assertFalse(parser._hasUserAgents)
        self.assertListEqual([], parser._userAgents)

    def test_getRandomUserAgent(self):
        parser = UserAgentParser()
        randomChoice = parser.getRandomUserAgent()
        self.assertIn(randomChoice, parser._userAgents)

    def test_getRandomUserAgentEvoke__createUserAgents(self):
        parser = UserAgentParser()
        parser.getRandomUserAgent()
        self.assertTrue(parser._hasUserAgents)
        self.assertNotEqual([], parser._userAgents)

    def test_getUserAgents(self):
        parser = UserAgentParser()
        userAgents = parser.getUserAgents()
        self.assertListEqual(userAgents, parser._userAgents)

    def test_getUserAgentsEvoke__createUserAgents(self):
        parser = UserAgentParser()
        parser.getUserAgents()
        self.assertTrue(parser._hasUserAgents)
        self.assertNotEqual([], parser._userAgents)

    def test_updateUserAgents(self):
        parser = UserAgentParser()
        parser.updateUserAgents()
        self.assertTrue(parser._hasUserAgents)
        self.assertNotEqual([], parser._userAgents)

    def test_createUserAgents(self):
        parser = UserAgentParser()
        parser._createUserAgents()
        self.assertTrue(parser._hasUserAgents)
        self.assertNotEqual([], parser._userAgents)

    def test_parseUserAgents(self):
        parser = UserAgentParser()
        someList = parser._parseUserAgents(parser.SOFTWARE['firefox'])
        self.assertIsInstance(someList, list)
        self.assertNotEqual([], someList)

    def test_parseUserAgentsRaisesExeption(self):
        parser = UserAgentParser()
        with self.assertRaises(ValueError):
            parser._parseUserAgents('Bad string')

    def test_appendToUserAgents(self):
        parser = UserAgentParser()
        firefox = parser._parseUserAgents(parser.SOFTWARE['firefox'])
        parser._appendToUserAgents(firefox)
        self.assertListEqual(firefox, parser._userAgents)

        opera = parser._parseUserAgents(parser.SOFTWARE['opera'])
        parser._appendToUserAgents(opera)
        for item in opera:
            self.assertIn(item, parser._userAgents)
        for item in firefox:
            self.assertIn(item, parser._userAgents)


if __name__ == '__main__':
    unittest.main()

