import unittest

from parsers.ProxyParser import ProxyParser


class ProxyParserTestCase(unittest.TestCase):
    def test_initialization(self):
        parser = ProxyParser()
        self.assertFalse(parser._ProxyParser__hasProxies)
        self.assertListEqual([], parser._ProxyParser__proxies)

    def test_clearProxies(self):
        parser = ProxyParser()
        parser.getProxies()
        parser._ProxyParser__clearProxies()
        self.assertFalse(parser._ProxyParser__hasProxies)
        self.assertListEqual([], parser._ProxyParser__proxies)

    def test_getRandomProxy(self):
        parser = ProxyParser()
        randomChoice = parser.getRandomProxy()
        self.assertIn(randomChoice, parser._ProxyParser__proxies)

    def test_getRandomProxyEvoke__createProxies(self):
        parser = ProxyParser()
        parser.getRandomProxy()
        self.assertTrue(parser._ProxyParser__hasProxies)
        self.assertNotEqual([], parser._ProxyParser__proxies)

    def test_getProxies(self):
        parser = ProxyParser()
        proxies = parser.getProxies()
        self.assertListEqual(proxies, parser._ProxyParser__proxies)

    def test_getProxiesEvoke__createProxies(self):
        parser = ProxyParser()
        parser.getProxies()
        self.assertTrue(parser._ProxyParser__hasProxies)
        self.assertNotEqual([], parser._ProxyParser__proxies)

    def test_updateProxies(self):
        parser = ProxyParser()
        parser.updateProxies()
        self.assertTrue(parser._ProxyParser__hasProxies)
        self.assertNotEqual([], parser._ProxyParser__proxies)

    def test_createProxies(self):
        parser = ProxyParser()
        parser._ProxyParser__createProxies()
        self.assertTrue(parser._ProxyParser__hasProxies)
        self.assertNotEqual([], parser._ProxyParser__proxies)

    def test_parseProxies(self):
        parser = ProxyParser()
        someList = parser._ProxyParser__parseProxies()
        self.assertIsInstance(someList, list)
        self.assertNotEqual([], someList)


if __name__ == '__main__':
    unittest.main()

