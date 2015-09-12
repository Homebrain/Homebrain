import threading


class Agent(threading.Thread):
    """
    The abstract class of all agents (InputSources, transformers/filters, OutputSources).

    This design is heavily inspired from ActivityWatch, check that to get an idea how the design looks.
    """

    @abstractmethod
    def run(self):
        pass
