from homebrain import Agent, Event, Dispatcher


class IDFilter(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""
    def __init__(self, ID, target=None):
        Agent.__init__(self)
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.id = ID

    def run(self):
        while True:
            event = self.next_event()
            print(event)
            if "id" in event and event["id"] == self.id:
                outgoing_event = Event(type=self.target, data=event["data"])
                self.dispatcher.post(outgoing_event)
