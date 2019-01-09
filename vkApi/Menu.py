# coding: utf-8

"""
Created on 25.08.2018

:author: Polianok Bogdan
"""


import itertools
import datetime

from vkApi.constants import cities
from vkApi.constants import ButtonsEnum
from vkApi.api import apiRequest
from core.RequestData import RequestData
from core.filters import filter_onlyCheapest


class Menu:
    def __init__(self, session):
        self.session = session
        self.keyboard = None

    def getKeyboard(self):
        return self.keyboard

    def getInstruction(self):
        return 'DEAFULT INSTRUCTION'

    def getValidActions(self):
        return [button['action']['label']
                for rowWithButtons in self.keyboard['buttons']
                for button in rowWithButtons
                ]


class MainMenu(Menu):
    def __init__(self, session):
        super().__init__(session)
        self.keyboard = {
            "one_time": False,
            "buttons": [
                [ButtonsEnum.source, ButtonsEnum.target],
                [ButtonsEnum.search]
            ]
        }

    def execute(self, action):
        if action == ButtonsEnum.source['action']['label']:
            self.session.changeMenu(SourceCityMenu(self.session))
        elif action == ButtonsEnum.target['action']['label']:
            self.session.changeMenu(TargetCityMenu(self.session))
        elif action == ButtonsEnum.search['action']['label']:
            if self.session.sourceCity and self.session.targetCity:
                self.session.changeMenu(SearchingMenu(self.session))

    def getInstruction(self):
        if not self.session.sourceCity and not self.session.targetCity:
            return 'Выберете город вылета и город прилета'
        elif not self.session.sourceCity:
            return 'Город прилета - {target}, выберете город вылета'.format(
                target=self.session.targetCity
            )
        elif not self.session.targetCity:
            return 'Город вылета - {source}, выберете город прилета'.format(
                source=self.session.sourceCity
            )
        else:
            return 'Город вылета - {source}, город прибытия - {target};'.format(
                source=self.session.sourceCity,
                target=self.session.targetCity
            )


class SourceCityMenu(Menu):
    def __init__(self, session):
        super().__init__(session)
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.back]]
        }

    def execute(self, action):
        if action == ButtonsEnum.back['action']['label']:
            self.session.changeMenu(MainMenu(self.session))
        elif action in cities.keys():
            self.session.sourceCity = action

    def getValidActions(self):
        return list(itertools.chain(
            super().getValidActions(),
            cities.keys(),
        ))

    def getInstruction(self):
        sourceCities = ',\n'.join(cities.keys())
        if self.session.sourceCity is not None:
            return 'Выбранный Вами город отправления - {sourceCity}.\n\n\n ' \
                   'Для изменения города отправьте сообщение с его названием:\n {cities}.'\
                .format(sourceCity=self.session.sourceCity, cities=sourceCities)
        else:
            return 'Отправьте сообщение с нужным городом:\n {cities}.'.format(
                cities=sourceCities
            )


class TargetCityMenu(Menu):
    def __init__(self, session):
        super().__init__(session)
        self.keyboard = {
            "one_time": False,
            "buttons": [[ButtonsEnum.back]]
        }

    def execute(self, action):
        if action == ButtonsEnum.back['action']['label']:
            self.session.changeMenu(MainMenu(self.session))
        elif action in cities.keys():
            self.session.targetCity = action

    def getValidActions(self):
        return list(itertools.chain(
            super().getValidActions(),
            cities.keys(),
        ))

    def getInstruction(self):
        targetCities = ',\n'.join(cities.keys())
        if self.session.targetCity is not None:
            return 'Выбранный Вами город прибытия - {targetCity}.\n\n\n ' \
                   'Для изменения города отправьте сообщение с его названием:\n {cities}.'\
                .format(targetCity=self.session.targetCity, cities=targetCities)
        else:
            return 'Отправьте сообщение с нужным городом:\n {cities}.'.format(
                cities=targetCities
            )


import threading
class Searcher(threading.Thread):
    def __init__(self, trip, session, filters):
        super().__init__()
        self.trip = trip
        self._is_running = True
        self.session = session
        self.filters = filters

    def run(self):
        maxPrice = 9999999
        for itineraries in self.session.scanner.scan(self.filters, trip=self.trip, useProxy=True):
            try:
                cheapestOption = itineraries[0].getCheapestPriceOptions()[0]
            except Exception as _:
                continue

            response = apiRequest('utils.getShortLink', {'url': cheapestOption.getLinkForBuying()})

            if int(cheapestOption) < maxPrice:
                maxPrice = int(cheapestOption)
                message = 'Pricing option: {option};\n\n Link: {link}'.format(
                    option=cheapestOption,
                    link=response['response']['short_url']
                )

                payload = {
                    'user_id': self.session.userId,
                    'message': message,
                }
                apiRequest('messages.send', payload)

            if not self._is_running:
                break

    def stop(self):
        self._is_running = False


class SearchingMenu(Menu):
    def __init__(self, session):
        super().__init__(session)
        self.keyboard = {
            "one_time": False,
            "buttons": [
                [ButtonsEnum.searchStart, ButtonsEnum.searchStop],
                [ButtonsEnum.back]
            ]
        }
        self.filters = [filter_onlyCheapest]

    def execute(self, action):
        if action == ButtonsEnum.back['action']['label']:
            self.session.changeMenu(MainMenu(self.session))
        elif action == ButtonsEnum.searchStart['action']['label']:
            trip = RequestData([{
                'origin': cities[self.session.sourceCity],
                'destination': cities[self.session.targetCity],
                'date': datetime.datetime.now().strftime("%Y-%m-%d")
            }])
            if self.session.thread:
                self.session.thread.stop()

            self.session.thread = Searcher(trip, self.session, self.filters)
            self.session.thread.start()
        elif action == ButtonsEnum.searchStop['action']['label']:
            self.session.thread.stop()


    def getInstruction(self):
        return 'TEXT'
        # self.session.changeMenu(MainMenu(self.session))
        # if self.session.sourceCity is not None and self.session.targetCity is not None:
        #     trip = RequestData([{
        #         'origin': cities[self.session.sourceCity],
        #         'destination': cities[self.session.targetCity],
        #         'date': datetime.datetime.now().strftime("%Y-%m-%d")
        #     }])
        #     maxPrice = 16000
        #     while True:
        #         for itineraries in self.session.scanner.scan(self.filters, trip=trip):
        #             try:
        #                 cheapestOption = itineraries[0].getCheapestPriceOptions()[0]
        #             except Exception as _:
        #                 return 'Рейсов по данным критериям не найдено.'
        #
        #             if int(cheapestOption) < maxPrice:
        #                 response = apiRequest('utils.getShortLink', {'url': cheapestOption.getLinkForBuying()})
        #                 return 'Pricing option: {option};\n\n Link: {link}'.format(
        #                     option=cheapestOption,
        #                     link=response['response']['short_url']
        #                 )

