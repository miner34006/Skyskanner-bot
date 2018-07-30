# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""


def filter_onlyDirect(itineraries):
    directItineraries = []
    for itinerary in itineraries:
        if itinerary.legs[0].stop_count == 0:
            directItineraries.append(itinerary)
    return directItineraries


def filter_onlyCheapest(itineraries, count=1):
    itineraries.sort(key=lambda x: x.getCheapestPriceOptions()[0])
    return itineraries[:count]


def filter_inPriceBorders(minPrice, maxPrice):
    pass