# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""

from functools import total_ordering

@total_ordering
class Price:
    """Class represented Price object in skyskanner website response

    """
    def __init__(self, jsonPrice):
        self.amount = jsonPrice.get('amount', None)
        self.last_updated = jsonPrice.get('last_updated', None)

        if self.amount is None:
            raise ValueError('Invalid amount in Price')

    def __str__(self):
        returnString = '(amount={amoumt}, last updated={last_updated})'\
            .format(amoumt=self.amount, last_updated=self.last_updated)
        return returnString

    def __int__(self):
        return int(self.amount)

    def __eq__(self, other):
        return self.amount == other.amount

    def __gt__(self, other):
        return self.amount > other.amount

