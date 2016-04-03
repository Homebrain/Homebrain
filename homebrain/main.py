import platform
import logging
import argparse
from time import sleep
import traceback
import getpass

from . import Dispatcher
from . import AgentManager, ModuleManager
from .api import WebSocket
from .logging import setup_logging


def run_chunker_example(dispatcher, am):
    """Needs the simulated lamp to be running in a different process, and expects the simulated button to fire."""
    from .agents.chunker.chunker import Chunker
    dispatcher.chain("button" , Chunker(5), ButtonListener())


def start():
    if getpass.getuser() == "root":
        print("Homebrain should not be run as root, exiting")
        exit()

    parser = argparse.ArgumentParser(description='The brain of your home')
    parser.add_argument('--debug', action='store_true', help='Sets loglevel to debug')
    args = parser.parse_args()

    # Initialize logger
    setup_logging(args.debug)

    # Initialize AgentManager for the first time (it's a singleton)
    am = AgentManager()

    # Initialize ModuleManager for the first time (it's a singleton)
    mm = ModuleManager()

    # Start the dispatcher
    Dispatcher().start()

    # Start APIs
    ws = WebSocket()
    ws.start()

    # Start Loggers
    am.start_agents()
