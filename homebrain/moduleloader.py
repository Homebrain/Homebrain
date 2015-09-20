import os
import sys
import importlib
import logging
import traceback
from homebrain.utils import get_cwd


def import_all_modules():
    """ Imports all modules, returns all agents to be autostarted """
    modules = os.listdir(get_cwd()+"/agents/") # Lists all folders in the agents directory
    sys.path.insert(0, get_cwd()+"/agents/") # Allows importlib to import from the agents directory

    agents = []
    autostartagents = []

    for module in modules:
        m = import_module(module)
        if m:
            agents.append(m.agentclass)
            if m.autostart:
                autostartagents.append(m.agentclass)
    logging.info("Loaded " + str(len(modules)) + " modules")

    initialized_agents = initialize_agents(autostartagents)
    logging.info("Initialized " + str(len(initialized_agents)) + " listener agents")

    return initialized_agents


def initialize_agents(agents: []):
    """ Inputs a list of classes to initialize, and returns a list of objects of the classes with default startup parameters """
    initialized_agents = []
    for agent in agents:
        initialized_agents.append(agent())
    return initialized_agents


def import_module(module_name: str):
    """ Tries to import a module, and returns the module object if it succeeds """
    module = None
    try:  # Import module
        m = importlib.import_module(module_name)
        if "autostart" in dir(m) and "agentclass" in dir(m):
            module = m
        #else:
        #    print("No autostart/agentclass in module " + module_name)
    except Exception as e:
        module = None
        logging.error("Couldn't import agent " + str(module_name) +
                      "\n" + traceback.format_exc())
    return module
