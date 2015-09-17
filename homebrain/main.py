import platform
import logging
import argparse
from time import sleep

from .dispatcher import Dispatcher

from . import AgentManager

# Import all agents
from .agents.chunker.chunker import Chunker
from .agents.lamphandler.lamphandler import LampHandler
from .agents.buttonlistener.buttonlistener import ButtonListener
from .agents.rest_listener.rest_listener import RestListener
from .agents.loglistener.loglistener import LogListener

def run_chunker_example(dispatcher, am):
    """Needs the simulated lamp to be running in a different process, and expects the simulated button to fire."""
    dispatcher.chain("button" , Chunker(5), ButtonListener())

def start():
    parser = argparse.ArgumentParser(description='The brain of your home')
    parser.add_argument('--debug', action='store_true', help='Sets loglevel to debug')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize AgentManager for the first time (it's a singleton)
    am = AgentManager()

    # TODO: Integrate this better into the rest of the system
    d = Dispatcher()
    d.start()
    RestListener().start()

    # Initialize Loggers and Wathcers
    bl = ButtonListener()
    d.bind(bl, "button")
    lh = LampHandler()
    d.bind(lh, "lamp")
    l = LogListener()
    d.bind(l, "log")

    # Add loggers and watchers to AgentManager
    am.add_agents([bl, lh, l])

    # run simulated demo agents
    #run_chunker_example(d, am)

    # Start Loggers
    am.start_agents()

    # Here we need to continue the main thread to prevent execution from terminating
    #while True:
    #    sleep(1)
