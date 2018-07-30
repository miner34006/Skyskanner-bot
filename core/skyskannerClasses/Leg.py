# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""


class Leg:
    """
    Class represented Leg object in skyskanner website response

    """

    def __init__(self, jsonLeg):
        self.id = jsonLeg['id']
        self.arrival = jsonLeg['arrival']
        self.departure = jsonLeg['departure']
        self.destination_place_id = jsonLeg['destination_place_id']
        self.duration = jsonLeg['duration']
        self.origin_place_id = jsonLeg['origin_place_id']
        self.stop_count = jsonLeg['stop_count']
