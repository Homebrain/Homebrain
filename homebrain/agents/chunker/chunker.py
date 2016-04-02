from homebrain import Agent, Event, Dispatcher
from homebrain.core.decorators import log_exceptions, stop_on_shutdown_event, log_events


class Chunker(Agent):
    """
    Listens to a certain trigger event, and emits a target event once the specified count has been reached.
    """

    autostart = False

    def __init__(self, count, target=None):
        super(Chunker, self).__init__()
        self.target = target if target is not None else self.identifier
        self.count = count
        self.events = []

    @stop_on_shutdown_event
    @log_events
    @log_exceptions
    def handle_event(self, event):
        self.events.append(event)
        if len(self.events) >= self.count:
            Dispatcher().put_event(
                Event(**{"tag": self.target,
                         "data": self.events}))
            self.events = []

    def cleanup(self):
        pass
