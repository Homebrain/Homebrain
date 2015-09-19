from homebrain import Agent, Dispatcher

class TemplateAgent(Agent):
    def __init__(self, target=None):
        super(TemplateAgent, self).__init__()
        self.target = target if target is not None else self.identifier
        Dispatcher().bind(self, "exampletype1")

    def run(self):
        while True:
            event = self.next_event()
            # Handle incoming events
