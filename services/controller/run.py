import sys
import os
import requests
import logging

from Controller import Controller

if __name__ == '__main__':
    logging.basicConfig(
        filename='/var/lib/skyscanner/logs/controller.log',
        format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logging.getLogger("requests").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)

    controller = Controller()
    controller.start()