import platform
import logging
import argparse
from time import sleep
import traceback

from .dispatcher import Dispatcher
from .moduleloader import *
from . import AgentManager


def run_chunker_example(dispatcher, am):
    """Needs the simulated lamp to be running in a different process, and expects the simulated button to fire."""
    from .agents.chunker.chunker import Chunker
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

    agents = load_all_modules()
    logging.info("Loaded " + str(len(agents)) + " agents, starting agents")

    # run simulated demo agents
    #run_chunker_example(d, am)

    am.add_agents(agents)

    # Start Loggers
    am.start_agents()

    # Here we need to continue the main thread to prevent execution from terminating
    #while True:
    #    sleep(1)
