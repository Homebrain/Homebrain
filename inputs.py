from agent import Agent

class InputSource(Agent):
    """
    The abstract class for input sources
    """

class WebSocketSource(InputSource):
    """
    Here we could start a WebSocket service that listens.
    """

class HTTPSource(InputSource):
    """
    Here we will bind in the REST API in some way.
    """
