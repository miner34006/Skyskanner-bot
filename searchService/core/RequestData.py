# coding: utf-8

"""
Created on 29.07.2018

:author: Polianok Bogdan
"""

import json


class RequestData:
    """
    class, needed to create json data for request

    """
    def __init__(self, legs, market='RU', currency='RUB', locale='ru-RU',
                 cabin_class='economy', prefer_directs=False, trip_type='one-way', adults='1',
                 child_ages=[], include_unpriced_itineraries=True, include_mixed_booking_options=True):

        self.legs = legs

        self.market = market
        self.currency = currency
        self.locale = locale
        self.cabin_class = cabin_class
        self.prefer_directs = prefer_directs
        self.trip_type = trip_type
        self.adults = adults
        self.child_ages = child_ages
        self.include_unpriced_itineraries = include_unpriced_itineraries
        self.include_mixed_booking_options = include_mixed_booking_options

    def getJsonRepresentation(self):
        """
        get json representation of data for request

        :return: data in json format
        :rtype: str
        """
        data = {
            'market': self.market, 'currency': self.currency, 'locale': self.locale, 'cabin_class': self.cabin_class,
            'prefer_directs': self.prefer_directs, 'trip_type': self.trip_type,
            'legs': [leg for leg in self.legs],
            'adults': self.adults, 'child_ages': self.child_ages,
            'options': {'include_unpriced_itineraries': self.include_unpriced_itineraries, 'include_mixed_booking_option': self.include_mixed_booking_options}
        }
        return json.dumps(data)

