from .util.event_thread import EventThread

class Dispatcher(EventThread):
    def __init__(self, agentmanager):
        EventThread.__init__(self)
        self._agentmanager = agentmanager

    def run(self):
        while True:
            self.process(self.next_event())

    def process(self, event):
        for subber in self._agentmanager.get_subscribers(event["type"]):
            subber.post(event)

"""
Not sure which code to use, commenting this out for others to review.

    bindings = {}

    def bind(self, agent, selector):
        if selector not in self.bindings.keys() or not self.bindings[selector]:
            self.bindings[selector] = set()

        self.bindings[selector].add(agent)

    def _query_selector(self, selector):
        "Returns all the agents that match the selector"
        return self.bindings[selector]

    def process(self, msg):
        handlers = _get_handlers(event["type"])
        for handler in handlers:
            handler.add_message(msg)

"""
