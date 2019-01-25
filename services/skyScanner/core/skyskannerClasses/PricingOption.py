# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""

import sys
import os
from functools import total_ordering

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from skyScanner.core.skyskannerClasses.Item import Item
from skyScanner.core.skyskannerClasses.Price import Price


@total_ordering
class PricingOption:
    """
    Class represented Pricing Option object in skyskanner website response

    """
    def __init__(self, jsonPricingOption):
        self.agent_ids = [id for id in jsonPricingOption['agent_ids']]
        self.items = [Item(item) for item in jsonPricingOption['items']]
        self.price = Price(jsonPricingOption['price'])

    def __str__(self):
        returnString = 'agents=[{agent_ids}], price={price}'\
            .format(agent_ids=','.join(self.agent_ids), price=str(self.price))
        return returnString

    def __int__(self):
        return int(self.price)

    def __eq__(self, other):
        return self.price == other.price

    def __gt__(self, other):
        return self.price > other.price

    def getLinkForBuying(self):
        """
        get a link on which you can buy a ticket

        :return: link to the market
        :rtype: str
        """
        return 'https://www.skyscanner.ru' + self.items[0].url

