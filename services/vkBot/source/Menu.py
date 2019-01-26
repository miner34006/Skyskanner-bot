# coding: utf-8

"""
Created on 25.08.2018

:author: Polianok Bogdan
"""

import sys
import os
import logging
import datetime

import requests

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from vkBot.source.constants import ButtonsEnum, cities
from modules.api import apiRequest

logger = logging.getLogger(__name__)


class Menu:
    """
    Class represented menu for vkApi bot
    """
    def __init__(self):
        self.keyboard = None

    def getKeyboard(self):
        """
        Get keyboard dict specific for menu object

        :return: keyboard dict for vkApi
        :rtype: dict
        """
        return self.keyboard

    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        raise NotImplemented


class MainMenu(Menu):
    """
    Menu for MainMenu state
    """
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [
                [ButtonsEnum.CHANGE_TEMPLATE],
                [ButtonsEnum.SEARCH_START, ButtonsEnum.SEARCH_STOP]
            ]
        }

    def _startSearch(self, session):
        """
        Start search event

        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if not session.date or not session.price or not session.sourceCity or not session.targetCity:
            logger.warning('Not enough data for searching')
            payload = {
                'user_id': session.userId,
                'message': 'Введены не все данные, заполните шаблон и попробуйте снова.\n\n',
            }
            apiRequest('messages.send', payload)
        else:
            response = requests.get('http://172.20.128.4:5001/search/{0}'.format(session.userId))
            if response.status_code == 200:
                requests.delete('http://172.20.128.4:5001/search/{0}'.format(session.userId))

            data = {
                'sourceCity': session.sourceCity,
                'targetCity': session.targetCity,
                'price': session.price,
                'date': session.date,
                'userId': session.userId
            }
            requests.post('http://172.20.128.4:5001/search', json=data)

    def _notifyUserAboutCurrentSearch(self, session):
        """
        Notify user, if he is searching tickets now

        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        try:
            logger.info('Getting information about current search')
            response = requests.get('http://172.20.128.4:5001/search/{0}'.format(session.userId))
            if response.status_code == 200:
                searchingInfo = 'В данный момент происходит поиск билета из {sourceCity} в {targetCity}, дата - {date}'.format(
                    sourceCity=response.json()['sourceCity'],
                    targetCity=response.json()['targetCity'],
                    date=response.json()['date']
                )
                payload = {
                    'user_id': session.userId,
                    'message': searchingInfo,
                }
                logger.info('Sending data about current search')
                apiRequest('messages.send', payload)

        except requests.exceptions.RequestException as e:
            logger.error(e)

    def execute(self, action, session):
        """
        Execute actions specific for menu object, depending on user action

        :param action: user action
        :type action: str
        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if action == ButtonsEnum.CHANGE_TEMPLATE['action']['label']:
            logger.info('Execute <CHANGE_TEMPLATE> action')
            session.changeMenu(SourceCitySelection())

        elif action == ButtonsEnum.SEARCH_START['action']['label']:
            logger.info('Execute <SEARCH_START> action')
            self._startSearch(session)

        elif action == ButtonsEnum.SEARCH_STOP['action']['label']:
            logger.info('Execute <SEARCH_STOP> action')
            requests.delete('http://172.20.128.4:5001/search/{0}'.format(session.userId))
        else:
            logger.info('Execute <INCORRECT_MAIN_MENU> action')

        self._notifyUserAboutCurrentSearch(session)


    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: instruction for user
        :rtype: str
        """
        return 'Город отправления - {sourceCity},\n' \
               'Город прибытия - {targetCity},\n' \
               'Дата поездки - {date},\n' \
               'Максимальная цена - {price}.\n'.format(
                    sourceCity=session.sourceCity if session.sourceCity else 'НЕ ЗАДАНО',
                    targetCity=session.targetCity if session.targetCity else 'НЕ ЗАДАНО',
                    date = session.date if session.date else 'НЕ ЗАДАНО',
                    price = session.price if session.price else 'НЕ ЗАДАНО'
                )


class SourceCitySelection(Menu):
    """
    Menu for source city selection
    """
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.BACK, ButtonsEnum.NEXT]]
        }

    def execute(self, action, session):
        """
        Execute actions specific for menu object, depending on user action

        :param action: user action
        :type action: str
        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if action == ButtonsEnum.BACK['action']['label']:
            logger.info('Execute <BACK> action')
            session.changeMenu(MainMenu())

        elif action == ButtonsEnum.NEXT['action']['label']:
            logger.info('Execute <NEXT> action')
            session.changeMenu(TargetCitySelection())

        elif action in cities:
            logger.info('Execute <SETUP_SOURCE_CITY> action')
            session.sourceCity = action
            session.changeMenu(TargetCitySelection())
        else:
            logger.info('Execute <INCORRECT_SOURCE_CITY> action')
            payload = {
                'user_id': session.userId,
                'message': 'Некорректное имя города.'
            }
            apiRequest('messages.send', payload)

    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: instruction for user
        :rtype: str
        """
        return 'Выбранный Вами город ОТПРАВЛЕНИЯ - {sourceCity}.\n\n\n'\
               'Для изменения города отправьте сообщение с его названием:\n{cities}.'.format(
                    sourceCity=session.sourceCity if session.sourceCity else 'НЕ ЗАДАНО',
                    cities=',\n'.join(cities)
               )


class TargetCitySelection(Menu):
    """
    Menu for target city selection
    """
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.BACK, ButtonsEnum.NEXT]]
        }

    def execute(self, action, session):
        """
        Execute actions specific for menu object, depending on user action

        :param action: user action
        :type action: str
        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if action == ButtonsEnum.BACK['action']['label']:
            logger.info('Execute <BACK> action')
            session.changeMenu(SourceCitySelection())

        elif action == ButtonsEnum.NEXT['action']['label']:
            logger.info('Execute <NEXT> action')
            session.changeMenu(DateSelection())

        elif action in cities:
            logger.info('Execute <SETUP_TARGET_CITY> action')
            session.targetCity = action
            session.changeMenu(DateSelection())
        else:
            logger.info('Execute <INCORRECT_TARGET_CITY> action')
            payload = {
                'user_id': session.userId,
                'message': 'Некорректное имя города.'
            }
            apiRequest('messages.send', payload)

    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: instruction for user
        :rtype: str
        """
        return 'Выбранный Вами город ПРИБЫТИЯ - {targetCity}.\n\n\n'\
               'Для изменения города отправьте сообщение с его названием:\n{cities}.'.format(
                    targetCity=session.targetCity if session.targetCity else 'НЕ ЗАДАНО',
                    cities=',\n'.join(cities)
               )


class DateSelection(Menu):
    """
    Menu for date selection
    """
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.BACK, ButtonsEnum.NEXT]]
        }

    def execute(self, action, session):
        """
        Execute actions specific for menu object, depending on user action

        :param action: user input action
        :type action: str
        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if action == ButtonsEnum.BACK['action']['label']:
            logger.info('Execute <BACK> action')
            session.changeMenu(TargetCitySelection())

        elif action == ButtonsEnum.NEXT['action']['label']:
            logger.info('Execute <NEXT> action')
            session.changeMenu(PriceSelection())

        elif self._dateIsValid(action):
            logger.info('Execute <SETUP_DATE> action')
            session.date = action
            session.changeMenu(PriceSelection())

        else:
            logger.info('Execute <INCORRECT_DATE> action')
            payload = {
                'user_id': session.userId,
                'message': 'Некорректный формат даты.',
            }
            apiRequest('messages.send', payload)

    def _dateIsValid(self, date):
        """
        Validate date from user input

        :param date: user date from input
        :type date: str
        :return: date validation status
        :rtype: bool
        """
        logger.info('Validating "{0}" date'.format(date))
        try:
            year, month, day = map(int, date.split('-'))
            datetime.date(year, month, day)
            return True
        except ValueError as e:
            logger.warning(e)
            return False

    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: instruction for user
        :rtype: str
        """
        return 'Выбранная Вами дата - {date}.\n\n\n' \
               'Для изменения ДАТЫ отправьте сообщение с датой в формате ГГГГ-ММ-ДД.'\
               .format(date=session.date if session.date else 'НЕ ЗАДАНО',)


class PriceSelection(Menu):
    """
    Menu for price selection
    """
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.BACK, ButtonsEnum.FINISH]]
        }

    def execute(self, action, session):
        """
        Execute actions specific for menu object, depending on user action

        :param action: user input action
        :type action: str
        :param session: UserSession object with data
        :type session: UserSession
        :return: None
        """
        if action == ButtonsEnum.BACK['action']['label']:
            logger.info('Execute <BACK> action')
            session.changeMenu(DateSelection())

        elif action == ButtonsEnum.FINISH['action']['label']:
            logger.info('Execute <NEXT> action')
            session.changeMenu(MainMenu())

        elif self._priceIsValid(action):
            logger.info('Execute <SETUP_PRICE> action')
            session.price = action
            session.changeMenu(MainMenu())

        else:
            logger.info('Execute <INCORRECT_PRICE> action')
            payload = {
                'user_id': session.userId,
                'message': 'Некорректный формат числа.\n\n'
            }
            apiRequest('messages.send', payload)

    def _priceIsValid(self, price):
        """
        Validate price from user input

        :param price: user date from input
        :type price: str
        :return: price validation status
        :rtype: bool
        """
        logger.info('Validating "{0}" price'.format(price))
        try:
            price = int(price)
            if price > 0:
                return True
            else:
                raise ValueError
        except ValueError as e:
            logger.warning(e)
            return False

    def getInstruction(self, session):
        """
        Get instruction specific for menu object

        :param session: UserSession object with data
        :type session: UserSession
        :return: instruction for user
        :rtype: str
        """
        return 'Выбранная Вами максимальная ЦЕНА билета - {price}.\n\n\n' \
               'Для изменения максимальной стоимости билета отправьте сообщение с числом:'\
               .format(price=session.price if session.price else 'НЕ ЗАДАНО')

