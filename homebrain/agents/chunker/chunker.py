from homebrain import Agent, Event

class Chunker(Agent):
    """Listens to a certain trigger event, and emits a target event once the specified count has been reached."""
    def __init__(self, dispatcher, count, trigger, target):
        Agent.__init__(self)
        self._subscriptions.append(trigger)
        self.dispatcher = dispatcher
        self.target = target
        self.count = count
        self.events = []

    def run(self):
        while True:
            event = self.next_event()
            self.events.append(event)
            print("n: " + str(len(self.events)))
            if len(self.events) >= self.count:
                self.dispatcher.post(Event(**{"type":self.target, "data": self.events}))
                self.events = []
