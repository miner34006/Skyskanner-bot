# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""


class Item:
    """
    Class represented Item object in skyskanner website response

    """
    def __init__(self, jsonItem):
        self.agent_id = jsonItem['agent_id']
        self.url = jsonItem['url']
        self.transfer_protection = jsonItem['transfer_protection']

