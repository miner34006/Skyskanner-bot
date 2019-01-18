import logging

from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

logging.basicConfig(
    filename='./logs/botService.log',
    format='[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
