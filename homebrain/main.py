import platform
import logging
import argparse
from time import sleep
import traceback

from .moduleloader import import_all_modules
from .dispatcher import Dispatcher
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

    # Import modules
    autostartagents = import_all_modules()
    # Add autostart agents
    am.add_agents(autostartagents)

    # run simulated demo agents
    #run_chunker_example(d, am)

    # Button with IDFilter example
    from .agents.idfilter.idfilter import IDFilter
    from .agents.lamphandler.lamphandler import LampHandler
    from .agents.ttshandler.ttshandler import TTSHandler
    # Initialize local clients
    locallamp = LampHandler("http://127.0.0.1:9090")
    localtts  = TTSHandler ("http://127.0.0.1:9092")
    # Toggle local light with "lightbin1"
    d.chain("button", IDFilter("lightbtn1"), locallamp)
    # Toggle local TTS with "ttsbtn1"
    d.chain("button", IDFilter("ttsbtn1"), localtts)

    # Start Loggers
    am.start_agents()
