# coding: utf-8

"""
Created on 30.07.2018

:author: Polianok Bogdan
"""

import sys
import os

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from skyScanner.core.skyskannerClasses.Leg import Leg


def findLegs(jsonData, legId):
    """
    find leg in json with ID

    :param jsonData: data where find leg
    :param legId: id of leg to find
    :return: leg object with legId
    :rtype" skyskannerClasses.Leg.Leg
    """
    return [Leg(leg) for leg in jsonData['legs'] if leg['id'] == legId]

