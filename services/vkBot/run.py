import sys
import os

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from vkBot.source.views import *

app.run(use_reloader=False, host='0.0.0.0', port=5000)
