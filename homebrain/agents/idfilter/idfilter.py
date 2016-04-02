from homebrain import Agent, Event, Dispatcher


class IDFilter(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""

    autostart = False

    def __init__(self, ID, target=None):
        Agent.__init__(self)
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.id = ID

    def handle_event(self, event):
        if "id" in event and event["id"] == self.id:
            outgoing_event = Event(tag=self.target, data=event["data"])
            self.dispatcher.put_event(outgoing_event)
