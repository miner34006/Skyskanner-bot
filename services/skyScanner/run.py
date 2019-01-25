import sys
import os

skyenv = os.environ.get('SKYENV', '/home/skyenv/')
sys.path.append(skyenv)

from skyScanner.searchingEngine.views import *

app.run(use_reloader=False, port=2000)
