# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""

from core.skyskannerClasses.PricingOption import PricingOption


class Itinerary:
    """Class represented Itinerary object in skyskanner website response

    """
    def __init__(self, jsonItinerary):
        self.id = jsonItinerary['id']
        self.leg_ids = [id for id in jsonItinerary['leg_ids']]

        self.pricing_options = []
        for option in jsonItinerary['pricing_options']:
            try:
                self.pricing_options.append(PricingOption(option))
            except ValueError:
                continue

    def __str__(self):
        returnString = \
            'Itinerary:\n\tid = {id},\n\tleg ids = [{leg_ids}],\n\tpricing options = [\n\t\t{pricing_options}\n\t]'.format(
            id=self.id,
            leg_ids=','.join(self.leg_ids),
            pricing_options=',\n\t\t'.join([str(option) for option in self.pricing_options]))

        return returnString

    def getCheapestPriceOption(self):
        """get the cheapest PricingOption from Itinerary.pricing_options

        :return: cheapest PricingOption
        :rtype: skyskannerClasses.PricingOption.PricingOption
        """
        priceOption = None
        for option in self.pricing_options:
            if (priceOption is None) or (option < priceOption):
                priceOption = option
        return priceOption

