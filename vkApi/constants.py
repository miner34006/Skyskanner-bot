# coding: utf-8

"""
Created on 25.08.2018

:author: Polianok Bogdan
"""

ADD_MESSAGE = 4


class ButtonsEnum:
    """
    Enum with different button types
    """
    back = {
        'action': {
            'type': 'text',
            'label': 'Назад',
        },
        'color': 'negative'
    }

    source = {
        'action': {
            'type': 'text',
            'label': 'Откуда',
        },
        'color': 'primary'
    }

    target = {
        'action': {
            'type': 'text',
            'label': 'Куда',
        },
        'color': 'primary'
    }

    search = {
        'action': {
            'type': 'text',
            'label': 'Показать самые дешевый билет',
        },
        'color': 'positive'
    }


cities = {
    'Владивосток': 'VVO',
    'Москва': 'MOSC',
    'Санкт-Петербург': 'LED',
    'Сочи': 'AAQ',
    'Екатеринбург': 'SVX',
    'Париж': 'PARI',
    'Ярославль': 'IAR',
}

