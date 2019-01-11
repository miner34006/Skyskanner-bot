# coding: utf-8

"""
Created on 22.09.2018

:author: Polianok Bogdan
"""

from vkApi.Menu import MainMenu


class UserSession:
    """
    class represented one session with single unique user (one session for each user)
    """
    def __init__(self, userId, scanner):

        # TODO get/set data from/to DB
        self._sourceCity = None
        self._targetCity = None

        self.userId = userId
        self.thread = None

        self.menu = MainMenu(self)
        self.scanner = scanner

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
        return self.menu.getInstruction()

    def changeMenu(self, menu):
        """
        Changing menu state
        :param menu: new menu state
        :return: None
        """
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
        self.menu.execute(action)

