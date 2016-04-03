from homebrain import Agent, Event, Dispatcher


class IDFilter(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""

    autostart = False

    def __init__(self, ID):
        Agent.__init__(self)
        self.dispatcher = Dispatcher()
        self.id = ID

    def handle_event(self, event):
        if "id" in event and event["id"] == self.id:
            self.dispatcher.put_event(event)
