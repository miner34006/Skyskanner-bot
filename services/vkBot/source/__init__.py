import sys
import os
import logging

import requests
from flask import Flask

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

import vkBot.config as config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

logging.basicConfig(
    filename='/var/lib/skyscanner/logs/vkBot.log',
    format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
