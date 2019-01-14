# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""


def filter_onlyDirect(itineraries):
    """
    filter the input itineraries and select only direct (stop count = 0)

    :param itineraries: input itineraries
    :return: direct itineraries
    :rtype: list
    """
    return [itinerary for itinerary in itineraries if itinerary.legs[0].stop_count == 0]


def filter_onlyCheapest(itineraries, count=1):
    """
    filter the input itineraries and select the cheapest one

    :param itineraries: input itineraries
    :param count: number of itineraries needed to get after filtering
    :return: cheapest itineraries
    :rtype: list
    """
    itineraries.sort(key=lambda x: x.getCheapestPriceOptions()[0])
    return itineraries[:count]


def filter_inPriceBorders(itineraries, minPrice, maxPrice):
    """
    filter the input itineraries and select itineraries with price from minPrice to maxPrice

    :param itineraries: input itineraries
    :param minPrice: minimum price for itinerary
    :param maxPrice: maximum price for itinerary
    :return: tineraries with price from minPrice to maxPrice
    :rtype: list
    """
    return [
        itinerary
        for itinerary in itineraries
        if minPrice <= itinerary.getCheapestPriceOptions()[0] <= maxPrice
    ]