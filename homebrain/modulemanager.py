import logging
import os
import sys
import importlib
import logging
import traceback
import getpass
import inspect

from .agentmanager import *
from .utils import Singleton, get_cwd

@Singleton
class ModuleManager:
    def __init__(self):
        self._modules = []
        self._import_all()


    @property
    def modules(self) -> []:
        """ Contains the set loaded agent modules """
        return self._modules


    def import_module(self, module_name: str):
        """ Tries to import a module, and returns the module object if it succeeds """
        try:  # Import module
            m = importlib.import_module(module_name)
            # Iterate over all module variables
            for name, aclass in inspect.getmembers(m):
                # Find all Agents classes
                if inspect.isclass(aclass) and issubclass(aclass, Agent):
                    # Add agent to list of modules
                    self._modules.append(aclass)
                    # If autostart static variable is not defined, default to false
                    aclass.autostart = getattr(aclass, 'autostart', False)
                    # If autostart var is true, add agent to agentmanager for autostart
                    if aclass.autostart:
                        AgentManager().add_agent(aclass())
        except Exception as e:
            module = None
            logging.error("Couldn't import module " + str(module_name) +
                          "\n" + traceback.format_exc())


    def _include_folder(self, path):
        sys.path.insert(0, path) # Allows importlib to import from the agents directory


    def _import_folder(self, path):
        moduledirs = os.listdir(path) # Lists all folders in the agents directory
        self._include_folder(path)

        for moduledir in moduledirs:
            agents = self.import_module(moduledir)


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
