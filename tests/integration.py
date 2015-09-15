import unittest
import threading
from subprocess import Popen, PIPE
import time

from homebrain import Agent, AgentManager, Dispatcher, Event
from homebrain.agents.chunker.chunker import Chunker
from homebrain.agents.simlamphandler.simlamphandler import SimLampHandler

from queue import Queue, Empty

class BackgroundReader(object):
    """Gathers lines from a stream in a background thread."""
    def __init__(self, stream):
        """Reads all lines from stream and puts them in a queue."""
        self.q = Queue()
        self.s = stream

        def readLoop(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                    print("line: %s" % line)
                else:
                    raise ValueError("Unexpected end of stream.")

        self.t = threading.Thread(target = readLoop, args = (self.s, self.q))
        self.t.daemon = True
        self.t.start()

    def readline(self, timeout = None):
        try:
            return self.q.get(block = timeout is not None, timeout = timeout)
        except Empty:
            return None

    def read_as_string(self):
        total = []
        self.s.flush()
        while not self.q.empty():
            total.append(self.q.get_nowait())
        return "\n".join(total)



class SimLampHW(threading.Thread):
    def run(self):
        self.running = True
        self.queue = Queue()
        self.process = Popen(["python3", "./homebrain/clients/simulatedlamp.py"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.stdout = BackgroundReader(self.process.stdout)
        while self.running:
            time.sleep(0.1)
        self.process.kill()

    def stop(self):
        self.running = False


def send_button_press():
    process = Popen(["python3", "./homebrain/clients/simulatedlamp.py"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    process.wait()

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.am = AgentManager()
        self.dispatcher = Dispatcher()
        self.dispatcher.daemon = True
        self.dispatcher.start()
        self.simlamphw = SimLampHW()
        self.simlamphw.daemon = True
        self.simlamphw.start()
        time.sleep(0.1) # Give the thread time to initialize

    def test_chain(self):
        self.dispatcher.chain("button" , Chunker(3), SimLampHandler("http://localhost:9090/"))
        time.sleep(0.1)
        self.assertNotIn("lamp is", self.simlamphw.stdout.read_as_string())
        send_button_press()
        time.sleep(0.1)
        self.assertNotIn("lamp is", self.simlamphw.stdout.read_as_string())
        send_button_press()
        time.sleep(0.1)
        self.assertNotIn("lamp is", self.simlamphw.stdout.read_as_string())
        send_button_press()
        time.sleep(0.1)
        self.assertIn("lamp is", self.simlamphw.stdout.read_as_string())
        self.simlamphw.stop()

    def tearDown(self):
        AgentManager.reset_singleton()
        Dispatcher.reset_singleton()
        self.simlamphw.stop()

