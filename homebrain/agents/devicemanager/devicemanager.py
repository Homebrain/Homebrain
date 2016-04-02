from homebrain import Agent, Dispatcher, AgentManager
from homebrain.core.decorators import stop_on_shutdown_event

from lamphandler import LampHandler
from ttshandler import TTSHandler
from idfilter import IDFilter
from clientagent import ClientAgent

import logging

class DeviceManager(Agent):

    autostart = True

    def __init__(self, target=None):
        super(DeviceManager, self).__init__()
        self.target = target if target is not None else self.identifier
        Dispatcher().bind(self, "add_client")
        
        self.clientc = 0
        
        self.lampc = 0
        self.ttsc = 0

    @stop_on_shutdown_event
    def handle_event(self, event):
        logging.info(event)
        if event["tag"] == "add_client":
            ip = event["data"]["ip"]
            port = event["data"]["port"]
            protocol = event["data"]["protocol"]
            name = "client"+str(self.clientc)
            client = ClientAgent(name, ip, port, protocol)
            self.clientc += 1
			
            for tag in event["data"]["tags"]:
                if tag == "lamp":
                    filterid = "lightbtn"+str(self.lampc)
                    self.lampc += 1
                    lamphandler = LampHandler(client)
                    lampfilter = IDFilter(filterid)
                    Dispatcher().chain("button", lampfilter, lamphandler)
                    logging.info("Added lamp for "+client.identifier)

                elif tag == "tts":
                    filterid = "ttsbtn"+str(self.ttsc)
                    self.ttsc += 1
                    ttshandler = TTSHandler(client)
                    ttsfilter = IDFilter(filterid)
                    Dispatcher().chain("button", ttsfilter, ttshandler)
                    logging.info("Added tts for "+client.identifier)
                
                AgentManager().start_agents()
