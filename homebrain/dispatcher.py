from .util.event_thread import EventThread

class Dispatcher(EventThread):

    def run(self):
        while True:
            self.process(self.next_event())

    def process(self, event):
        print(event)

