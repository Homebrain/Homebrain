import threading
from queue import Queue
class EventThread(threading.Thread):

    _mailbox= Queue()

    def post (self, msg):
        self._mailbox.put(msg)

    def next_event(self):
        return self._mailbox.get()
