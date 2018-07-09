# coding: utf-8

"""
Created on 09.07.2018

:author: Polianok Bogdan
"""


class Proxy:
    def __init__(self, ipAddress, port, https):
        self.ipAddress = ipAddress
        self.port = port
        self.https = https

    def __str__(self):
        return '{0}://{1}:{2}'.format(
            (lambda connection: 'https' if self.https == 'yes' else 'http')(self.https),
            self.ipAddress,
            self.port
        )
