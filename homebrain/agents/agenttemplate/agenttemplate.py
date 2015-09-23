from homebrain import Agent, Dispatcher

class TemplateAgent(Agent):
    def __init__(self, target=None):
        super(TemplateAgent, self).__init__()
        self.target = target if target is not None else self.identifier

        # Only bind manually if you are an endpoint agent. Otherwise, use Dispatcher.chain at config time.
        Dispatcher().bind(self, "exampletype1")

    @Agent.stop_on_shutdown_event
    def handle_event(self, event):
        # Handle incoming events
        pass
