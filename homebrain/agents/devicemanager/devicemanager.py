from homebrain import Agent, Dispatcher, AgentManager
from homebrain.core.decorators import stop_on_shutdown_event

from homebrain.agents.lamphandler import LampHandler
from homebrain.agents.ttshandler import TTSHandler
from homebrain.agents.idfilter import IDFilter

import logging

class DeviceManager(Agent):
    def __init__(self, target=None):
        super(DeviceManager, self).__init__()
        self.target = target if target is not None else self.identifier
        Dispatcher().bind(self, "add_lamp")
        Dispatcher().bind(self, "add_tts")
        self.lampc = 0
        self.ttsc = 0

    @stop_on_shutdown_event
    def handle_event(self, event):
        logging.info(event)
        if event["type"] == "add_lamp":
            filterid = "lightbtn"+str(self.lampc)
            lampid = event["data"]["ip"]+":"+event["data"]["port"]
            self.lampc += 1
            url = "http://"+event["data"]["ip"]+":"+event["data"]["port"]
            lamphandler = LampHandler(lampid, url)
            Dispatcher().chain("button", IDFilter(filterid), lamphandler)
            AgentManager().start_agents()
            logging.info("Added lamp at "+url)

        elif event["type"] == "add_tts":
            filterid = "ttsbtn"+str(self.ttsc)
            ttsid = event["data"]["ip"]+":"+event["data"]["port"]
            self.ttsc += 1
            url = "http://"+event["data"]["ip"]+":"+event["data"]["port"]
            ttshandler = TTSHandler(ttsid, url)
            Dispatcher().chain("button", IDFilter(filterid), ttshandler)
            AgentManager().start_agents()
            logging.info("Added tts client at "+url)
