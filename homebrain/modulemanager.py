from datetime import datetime
import logging
import os
import sys
import importlib
import logging
import traceback
from homebrain.utils import get_cwd

from .utils import Singleton

@Singleton
class ModuleManager:
    def __init__(self):
        self._agents = set()  # type: Set[Agent]
        self._modules = []    # type: []
        self._started = datetime.now()
        self._import_all()

    @property
    def modules(self) -> []:
        """ Contains the set loaded agent modules """
        return self._modules

    def _import_all(self):
        """ Imports all agents, returns an array of all loaded modules """
        moduledirs = os.listdir(get_cwd()+"/agents/") # Lists all folders in the agents directory
        sys.path.insert(0, get_cwd()+"/agents/") # Allows importlib to import from the agents directory

        for moduledir in moduledirs:
            module = self.import_module(moduledir)
            if module and hasattr(module, 'agentclass'):
                if hasattr(module, 'agentclass'):
                    self._modules.append(module)
                # If autostart is not set for module, default to false
                if not hasattr(module, 'autostart'):
                    module.autostart = False
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
