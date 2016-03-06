import logging
import os
import sys
import importlib
import logging
import traceback
import getpass

from .agentmanager import *
from .utils import Singleton, get_cwd

@Singleton
class ModuleManager:
    def __init__(self):
        self._modules = []    # type: []
        self._import_all()

    @property
    def modules(self) -> []:
        """ Contains the set loaded agent modules """
        return self._modules

    def start_autostart_agents(self):
        """ Starts all agents with autostart set to true """
        # Find and start all autostart modules
        startedagents = []
        for module in self.modules:
            if hasattr(module, 'autostart') and module.autostart == True:
                startedagents.append(module.agentclass())
        logging.info("Started " + str(len(startedagents)) + " listener agents")
        return startedagents

    def _include_folder(self, path):
        sys.path.insert(0, path) # Allows importlib to import from the agents directory

    def _import_folder(self, path):
        moduledirs = os.listdir(path) # Lists all folders in the agents directory
        self._include_folder(path)

        for moduledir in moduledirs:
            module = self.import_module(moduledir)
            if module and hasattr(module, 'agentclass'):
                if hasattr(module, 'agentclass'):
                    self._modules.append(module)
                # If autostart is not set for module, default to false
                if not hasattr(module, 'autostart'):
                    module.autostart = False

    def _import_all(self):
        """ Imports all agents, returns an array of all loaded modules """
        user = getpass.getuser()

        # System agent folder
        systemagentdir = get_cwd()+"/agents/"

        # Get user agent folder
        useragentdir = ""
        if user == "homebrain":
            useragentdir = "/var/lib/homebrain/agents/"
        else:
            homedir = os.path.expanduser("~")
            useragentdir = homedir+"/.config/homebrain/agents/"

        # Include agent folders
        self._include_folder(systemagentdir)
        self._include_folder(useragentdir)

        # Import built-in agents
        try:
            self._import_folder(systemagentdir)
        except FileNotFoundError as err:
            logging.critical("ModuleManager: Built-in agent directory does not exist '{}'".format(systemagentdir))

        # Import user agents
        try:
            self._import_folder(useragentdir)
        except FileNotFoundError as err:
            logging.warning("ModuleManager: Users private agent directory does not exist '{}'".format(useragentdir))

        logging.info("Loaded " + str(len(self._modules)) + " modules")


    def import_module(self, module_name: str):
        """ Tries to import a module, and returns the module object if it succeeds """
        module = None
        try:  # Import module
            m = importlib.import_module(module_name)
            if "autostart" in dir(m) and "agentclass" in dir(m):
                module = m
            else:
                logging.error("Agentclass invalid in module " + module_name)
        except Exception as e:
            module = None
            logging.error("Couldn't import agent " + str(module_name) +
                          "\n" + traceback.format_exc())
        return module
