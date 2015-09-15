from homebrain import Agent, Event, Dispatcher

class Chunker(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""
    def __init__(self, count, target=None):
        Agent.__init__(self)
        self.target = target if target is not None else self.identifier
        self.count = count
        self.events = []

    def run(self):
        while True:
            event = self.next_event()
            self.events.append(event)
            if len(self.events) >= self.count:
                Dispatcher().post(Event(**{"type":self.target, "data": self.events}))
                self.events = []
