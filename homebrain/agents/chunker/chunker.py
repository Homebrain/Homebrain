from homebrain import ConveyorAgent, Event, Dispatcher


class Chunker(ConveyorAgent):
    """
    Listens to a certain trigger event, and emits a target event once the specified count has been reached.
    """

    def __init__(self, count, target=None):
        super(Chunker, self).__init__()
        self.target = target if target is not None else self.identifier
        self.count = count
        self.events = []

    @ConveyorAgent.stop_on_shutdown_event
    @ConveyorAgent.log_events
    @ConveyorAgent.log_exceptions
    def handle_event(self, event):
        self.events.append(event)
        if len(self.events) >= self.count:
            Dispatcher().post(
                Event(**{"type": self.target,
                         "data": self.events}))
            self.events = []

    def cleanup(self):
        pass
