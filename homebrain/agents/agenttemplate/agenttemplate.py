from homebrain import ConveyorAgent, Dispatcher

class TemplateAgent(ConveyorAgent):
    def __init__(self, target=None):
        super(TemplateAgent, self).__init__()
        self.target = target if target is not None else self.identifier

        # Only bind manually if you are an endpoint agent. Otherwise, use Dispatcher.chain at config time.
        Dispatcher().bind(self, "exampletype1")

    @ConveyorAgent.stop_on_shutdown_event
    def handle_event(self, event):
        # Handle incoming events
        pass
