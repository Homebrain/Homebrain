import platform
import logging
import argparse
from time import sleep

from dispatcher import Dispatcher
from modules.rest_listener.rest_listener import RestListener

from . import ModuleManager, rest

def start():
    parser = argparse.ArgumentParser(description='The brain of your home')
    parser.add_argument('--debug', action='store_true', help='Sets loglevel to debug')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize ModuleManager for the first time (it's a singleton)
    mm = ModuleManager()

    # TODO: Integrate this better into the rest of the system
    d = Dispatcher()
    d.start()
    RestListener(d).start()

    # Add loggers and watchers to ModuleManager
    mm.add_agents([])

    # Start Loggers
    mm.start_agents()

    rest.start_server()

    # Here we need to continue the main thread to prevent execution from terminating
    while True:
        sleep(1)
