from .util.event_thread import EventThread

class Dispatcher(EventThread):
    def __init__(self, agentmanager):
        super(Dispatcher, self).__init__()
        self._agentmanager = agentmanager

    def run(self):
        while True:
            self.process(self.next_event())

    def process(self, event):
        for subber in self._agentmanager.get_subscribers(event["type"]):
            subber.post(event)
