from homebrain import Agent, Event, Dispatcher

class ButtonListener(Agent):
    def __init__(self, dispatcher, target=None):
        super(ButtonListener, self).__init__()
        self.target = target if target is not None else self.identifier
        self.dispatcher = dispatcher

    def run(self):
        while True:
            event = self.next_event()
            data = {'data': {'action': "toggle"}}
            self.dispatcher.post(Event(type="lamp", data=data))
