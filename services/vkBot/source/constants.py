# coding: utf-8

"""
Created on 25.08.2018

:author: Polianok Bogdan
"""


class ButtonsEnum:
    """
    Enum with different button types
    """

    BACK = {
        'action': {
            'type': 'text',
            'label': 'Назад',
        },
        'color': 'negative'
    }

    SEARCH_START = {
        'action': {
            'type': 'text',
            'label': 'Начать поиск',
        },
        'color': 'positive'
    }

    SEARCH_STOP = {
        'action': {
            'type': 'text',
            'label': 'Остановить поиск',
        },
        'color': 'negative'
    }

    CHANGE_TEMPLATE = {
        'action': {
            'type': 'text',
            'label': 'Изменить шаблон поиска'
        },
        'color': 'primary'
    }

    NEXT = {
        'action': {
            'type': 'text',
            'label': 'Далее'
        },
        'color': 'primary'
    }

    FINISH = {
        'action': {
            'type': 'text',
            'label': 'Завершить'
        },
        'color': 'primary'
    }


cities = ['Владивосток', 'Москва', 'Санкт-Петербург', 'Сочи', 'Екатеринбург',
          'Париж', 'Ярославль', 'Прага', 'Рига', 'Берлин-Тегель',
          'Берлин-Шёнефельд', 'Мюнхен', 'Таллин', 'Хельсинки']
