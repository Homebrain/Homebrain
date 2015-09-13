from modulemanager import ModuleManager
import rest

from dispatcher import Dispatcher
from modules.rest_listener.rest_listener import RestListener

def start_dispatcher():
    d = Dispatcher()
    d.start()
    RestListener(d).start()

def start():
    import platform
    import logging
    import argparse

    parser = argparse.ArgumentParser(description='Logs your computer activities and much more. Built to be extended.')
    parser.add_argument('--debug', action='store_true', help='Sets loglevel to debug')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize ModuleManager for the first time (it's a singleton)
    mm = ModuleManager()

    # Add loggers and watchers to ModuleManager
    mm.add_agents([])

    # Start Loggers
    mm.start_agents()

    rest.start_server()

if __name__ == "__main__":
    start()
    start_dispatcher()
