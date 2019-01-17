# coding: utf-8

"""
Created on 22.09.2018

:author: Polianok Bogdan
"""

import logging
from json import JSONEncoder

import botService.vkBot.Menu as Menu

logger = logging.getLogger(__name__)


class UserSession:
    """
    class represented one session with single unique user (one session for each user)
    """
    def __init__(self, userId):
        self._sourceCity = None
        self._targetCity = None
        self.date = None
        self.price = None
        self.userId = userId
        self.menu = Menu.MainMenu()

    @property
    def sourceCity(self):
        """
        _sourceCity getter
        :return: _sourceCity
        :rtype: str
        """
        return self._sourceCity

    @sourceCity.setter
    def sourceCity(self, value):
        """
        _sourceCity setter
        :param value: new _sourceCity value
        :return: None
        """
        self._sourceCity = value

    @property
    def targetCity(self):
        """
        _targetCity getter
        :return: _targetCity
        :rtype: str
        """
        return self._targetCity

    @targetCity.setter
    def targetCity(self, value):
        """
        _targetCity setter
        :param value: new _targetCity value
        :return: None
        """
        self._targetCity = value

    def getKeyboard(self):
        """
        Getting keyboard
        :return: keyboard for current Menu
        :rtype: dict
        """
        return self.menu.getKeyboard()

    def getInstruction(self):
        """
        Getting instruction for user (text for user)
        :return: instruction for user
        :rtype: str
        """
        return self.menu.getInstruction(self)

    def changeMenu(self, menu):
        """
        Changing menu state
        :param menu: new menu state
        :return: None
        """
        logger.info('Change menu from {0} to {1}'.format(type(self.menu), type(menu)))
        self.menu = menu

    def getValidActions(self):
        """
        Getting valid actions for current Menu
        :return: valid actions
        :rtype: list
        """
        return self.menu.getValidActions()

    def execute(self, action):
        """
        Execute action for current menu (if it exists)
        :param action: action to execute
        :return: None
        """
        self.menu.execute(action, self)


class SessionEncoder(JSONEncoder):
    """
    Encoder for session object
    """
    def default(self, o):
        """ Function to encode UserSession object

        :param o: session object
        :type o: UserSession
        :return: session dict
        :rtype: dict
        """
        if isinstance(o, UserSession):
            logger.info('Encode user session object into dict')

        obj = o.__dict__
        obj.update({'class': type(o).__name__})
        return obj


def asSession(dict):
    """ Function to create UserSession object from dict

    :param dict: dict represented UserSession obj
    :type dict: dict
    :return: user session object
    :rtype: UserSession
    """
    if 'class' in dict and dict['class'] == 'UserSession':
        logger.info('Decode user session string into object')
        userSession = UserSession(dict['userId'])
        userSession.sourceCity = dict['_sourceCity']
        userSession.targetCity = dict['_targetCity']
        userSession.price = dict['price']
        userSession.date = dict['date']

        menuClass = getattr(Menu, dict['menu']['class'])
        menu = menuClass()
        userSession.menu = menu
        return userSession
    else:
        return dict
    