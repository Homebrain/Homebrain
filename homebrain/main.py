import platform
import logging
import argparse
import os, sys, inspect
import importlib
from homebrain.utils import *
from time import sleep

from .dispatcher import Dispatcher

from . import AgentManager

# Import all agents

def run_chunker_example(dispatcher, am):
    """Needs the simulated lamp to be running in a different process, and expects the simulated button to fire."""
    from .agents.chunker.chunker import Chunker
    dispatcher.chain("button" , Chunker(5), ButtonListener())

def load_agent(agentname):
    agent = None
    try: # Import module
        m = importlib.import_module(agentname)
    except Exception as e:
        print("Couldn't import agent " + agentname)
    if m and "agentclass" in dir(m):
        try: # Initialize Agent
            agent = m.agentclass()
        except Exception as e:
            logging.warning("Couldn't load agent " + agentname)
            print(e)
        # Setup bindings
        if "bindings" in dir(m):
            print("test")
            if type(m.bindings) is None:
                pass
            elif type(m.bindings) is str:
                print("bind " + m.bindings + " to " + str(agent))
                Dispatcher().bind(agent, m.bindings)
            elif type(m.bindings) is list:
                for binding in m.bindings:
                    print("bind " + binding + " to " + str(agent))
                    Dispatcher().bind(agent, binding)
    return agent

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

    modules = os.listdir(get_cwd()+"/agents/")
    sys.path.insert(0, get_cwd()+"/agents/")

    agents = []
    for module in modules:
        agent = load_agent(module)
        if agent:
            agents.append(agent)
    logging.info("Loaded " + str(len(agents)) + " agents, starting agents")

    # run simulated demo agents
    #run_chunker_example(d, am)

    am.add_agents(agents)

    # Start Loggers
    am.start_agents()

    # Here we need to continue the main thread to prevent execution from terminating
    #while True:
    #    sleep(1)
