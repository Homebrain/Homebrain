import os, sys
import importlib
from homebrain.utils import *

def load_all_modules():
    modules = os.listdir(get_cwd()+"/agents/")
    sys.path.insert(0, get_cwd()+"/agents/")
    agents = []
    for module in modules:
        agent = load_module(module)
        if agent:
            agents.append(agent)
    return agents

def load_module(agentname):
    agent = None
    m = None
    try: # Import module
        m = importlib.import_module(agentname)
    except Exception as e:
        logging.error("Couldn't import agent " + agentname +
                      "\n" + traceback.format_exc())
    if m and "agentclass" in dir(m):
        try: # Initialize Agent
            agent = m.agentclass()
        except Exception as e:
            logging.error("Couldn't load agent " + agentname +
                          "\n" + traceback.format_exc())
    return agent
