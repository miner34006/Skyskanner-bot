# coding: utf-8

"""
Created on 25.08.2018

:author: Polianok Bogdan
"""


import datetime
import itertools

from botService.vkBot.constants import ButtonsEnum, cities
from core.RequestData import RequestData
from core.filters import filter_onlyCheapest


class Menu:
    def __init__(self):
        self.keyboard = None

    def getKeyboard(self):
        return self.keyboard

    def getInstruction(self, session):
        return 'DEAFULT INSTRUCTION'

    def getValidActions(self):
        return [button['action']['label']
                for rowWithButtons in self.keyboard['buttons']
                for button in rowWithButtons
                ]


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [
                [ButtonsEnum.source, ButtonsEnum.target],
                [ButtonsEnum.search]
            ]
        }

    def execute(self, action, session):
        if action == ButtonsEnum.source['action']['label']:
            session.changeMenu(SourceCityMenu())
        elif action == ButtonsEnum.target['action']['label']:
            session.changeMenu(TargetCityMenu())
        elif action == ButtonsEnum.search['action']['label']:
            if session.sourceCity and session.targetCity:
                session.changeMenu(SearchingMenu())

    def getInstruction(self, session):
        if not session.sourceCity and not session.targetCity:
            return 'Выберете город вылета и город прилета'
        elif not session.sourceCity:
            return 'Город прилета - {target}, выберете город вылета'.format(
                target=session.targetCity
            )
        elif not session.targetCity:
            return 'Город вылета - {source}, выберете город прилета'.format(
                source=session.sourceCity
            )
        else:
            return 'Город вылета - {source}, город прибытия - {target};'.format(
                source=session.sourceCity,
                target=session.targetCity
            )


class SourceCityMenu(Menu):
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.back]]
        }

    def execute(self, action, session):
        if action == ButtonsEnum.back['action']['label']:
            session.changeMenu(MainMenu())
        elif action in cities.keys():
            session.sourceCity = action

    def getValidActions(self):
        return list(itertools.chain(
            super().getValidActions(),
            cities.keys(),
        ))

    def getInstruction(self, session):
        sourceCities = ',\n'.join(cities.keys())
        if session.sourceCity is not None:
            return 'Выбранный Вами город отправления - {sourceCity}.\n\n\n ' \
                   'Для изменения города отправьте сообщение с его названием:\n {cities}.'\
                .format(sourceCity=session.sourceCity, cities=sourceCities)
        else:
            return 'Отправьте сообщение с нужным городом:\n {cities}.'.format(
                cities=sourceCities
            )


class TargetCityMenu(Menu):
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.back]]
        }

    def execute(self, action, session):
        if action == ButtonsEnum.back['action']['label']:
            session.changeMenu(MainMenu())
        elif action in cities.keys():
            session.targetCity = action

    def getValidActions(self):
        return list(itertools.chain(
            super().getValidActions(),
            cities.keys(),
        ))

    def getInstruction(self, session):
        targetCities = ',\n'.join(cities.keys())
        if session.targetCity is not None:
            return 'Выбранный Вами город прибытия - {targetCity}.\n\n\n ' \
                   'Для изменения города отправьте сообщение с его названием:\n {cities}.'\
                .format(targetCity=session.targetCity, cities=targetCities)
        else:
            return 'Отправьте сообщение с нужным городом:\n {cities}.'.format(
                cities=targetCities
            )

class SearchingMenu(Menu):
    def __init__(self):
        super().__init__()
        self.keyboard = {
            "one_time": False,
            "buttons": [
                [ButtonsEnum.searchStart, ButtonsEnum.searchStop],
                [ButtonsEnum.back]
            ]
        }
        self.filters = [filter_onlyCheapest]

    def execute(self, action, session):
        pass