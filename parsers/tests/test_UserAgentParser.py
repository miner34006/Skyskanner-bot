import unittest

from parsers.UserAgentParser import UserAgentParser


class UserAgentParserTestCase(unittest.TestCase):
    def test_initialization(self):
        parser = UserAgentParser()
        self.assertFalse(parser._UserAgentParser__hasUserAgents)
        self.assertListEqual([], parser._UserAgentParser__userAgents)

    def test_clearUserAgents(self):
        parser = UserAgentParser()
        parser._UserAgentParser__clearUserAgents()
        self.assertFalse(parser._UserAgentParser__hasUserAgents)
        self.assertListEqual([], parser._UserAgentParser__userAgents)

    def test_getRandomUserAgent(self):
        parser = UserAgentParser()
        randomChoice = parser.getRandomUserAgent()
        self.assertIn(randomChoice, parser._UserAgentParser__userAgents)

    def test_getRandomUserAgentEvoke__createUserAgents(self):
        parser = UserAgentParser()
        parser.getRandomUserAgent()
        self.assertTrue(parser._UserAgentParser__hasUserAgents)
        self.assertNotEqual([], parser._UserAgentParser__userAgents)

    def test_getUserAgents(self):
        parser = UserAgentParser()
        userAgents = parser.getUserAgents()
        self.assertListEqual(userAgents, parser._UserAgentParser__userAgents)

    def test_getUserAgentsEvoke__createUserAgents(self):
        parser = UserAgentParser()
        parser.getUserAgents()
        self.assertTrue(parser._UserAgentParser__hasUserAgents)
        self.assertNotEqual([], parser._UserAgentParser__userAgents)

    def test_updateUserAgents(self):
        parser = UserAgentParser()
        parser.updateUserAgents()
        self.assertTrue(parser._UserAgentParser__hasUserAgents)
        self.assertNotEqual([], parser._UserAgentParser__userAgents)

    def test_createUserAgents(self):
        parser = UserAgentParser()
        parser._UserAgentParser__createUserAgents()
        self.assertTrue(parser._UserAgentParser__hasUserAgents)
        self.assertNotEqual([], parser._UserAgentParser__userAgents)

    def test_parseUserAgents(self):
        parser = UserAgentParser()
        someList = parser._UserAgentParser__parseUserAgents(parser.SOFTWARE['firefox'])
        self.assertIsInstance(someList, list)
        self.assertNotEqual([], someList)

    def test_parseUserAgentsRaisesExeption(self):
        parser = UserAgentParser()
        with self.assertRaises(ValueError):
            parser._UserAgentParser__parseUserAgents('Bad string')

    def test_appendToUserAgents(self):
        parser = UserAgentParser()
        firefox = parser._UserAgentParser__parseUserAgents(parser.SOFTWARE['firefox'])
        parser._UserAgentParser__appendToUserAgents(firefox)
        self.assertListEqual(firefox, parser._UserAgentParser__userAgents)

        opera = parser._UserAgentParser__parseUserAgents(parser.SOFTWARE['opera'])
        parser._UserAgentParser__appendToUserAgents(opera)
        for item in opera:
            self.assertIn(item, parser._UserAgentParser__userAgents)
        for item in firefox:
            self.assertIn(item, parser._UserAgentParser__userAgents)


if __name__ == '__main__':
    unittest.main()

