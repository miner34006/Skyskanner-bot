# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""

from core.skyskannerClasses.PricingOption import PricingOption


class Itinerary:
    """
    Class represented Itinerary object in skyskanner website response

    """
    def __init__(self, jsonItinerary, legs=[]):
        self.id = jsonItinerary['id']
        self.legs = legs

        self.pricing_options = []
        for option in jsonItinerary['pricing_options']:
            try:
                self.pricing_options.append(PricingOption(option))
            except ValueError:
                continue

    def __str__(self):
        returnString = \
            'Itinerary:\n\tid = {id},\n\tpricing options = [\n\t\t{pricing_options}\n\t]'.format(
            id=self.id,
            pricing_options=',\n\t\t'.join([str(option) for option in self.pricing_options]))

        return returnString

    def getCheapestPriceOptions(self):
        """
        get the cheapest PricingOption from Itinerary.pricing_options

        :return: cheapest PricingOptions
        :rtype: list
        """
        self.pricing_options.sort(key=lambda x: x.price)

        cheapestOption = [self.pricing_options[0]]
        for option in self.pricing_options:
            if option == cheapestOption[0]:
                cheapestOption.append(option)
            else:
                break

        return cheapestOption

