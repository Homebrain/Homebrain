import platform
import logging
import argparse
from time import sleep

from .dispatcher import Dispatcher
from .agents.rest_listener.rest_listener import RestListener

from . import AgentManager

def run_chunker_example(dispatcher, am):
    """Needs the simulated lamp to be running in a different process, and expects the simulated button to fire."""
    from .agents.chunker.chunker import Chunker
    from .agents.simlamphandler.simlamphandler import SimLampHandler
    chunker = Chunker(dispatcher, 5, "button", "5_button_presses")
    lamp = SimLampHandler(dispatcher, "5_button_presses", "http://localhost:9090/")
    am.add_agents([chunker, lamp])


def start():
    parser = argparse.ArgumentParser(description='The brain of your home')
    parser.add_argument('--debug', action='store_true', help='Sets loglevel to debug')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize AgentManager for the first time (it's a singleton)
    am = AgentManager()

    # TODO: Integrate this better into the rest of the system
    d = Dispatcher(am)
    d.start()
    RestListener(d).start()

    # Add loggers and watchers to AgentManager
    am.add_agents([])

    # run simulated demo agents
    run_chunker_example(d, am)

    # Start Loggers
    am.start_agents()


    # Here we need to continue the main thread to prevent execution from terminating
    while True:
        sleep(1)
