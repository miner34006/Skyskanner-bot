import config
from flask import Flask

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

handler = RotatingFileHandler(app.config['LOGFILE'], maxBytes=1000000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)
