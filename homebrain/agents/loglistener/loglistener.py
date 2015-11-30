from collections import defaultdict
from homebrain import Agent, Dispatcher
import logging


class LogListener(Agent):
    def __init__(self, target=None):
        super(LogListener, self).__init__()
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.unknown_logger = logging.getLogger("Unknown Client")

    def handle_event(self, event):
        data = event["data"]
        msg = data["msg"]
        # Origin
        if "origin" in event:
            origin = event["origin"]["name"]
            logger = logging.getLogger(origin)
        else:
            logger = self.unknown_logger
        # Level
        if "level" in data:
            levelstr = data["level"].lower()
            levelmap = defaultdict(None)
            levelmap.extend({"debug": logging.DEBUG,
                             "info": logging.INFO,
                             "warning": logging.WARNING,
                             "error": logging.ERROR,
                             "critical": logging.CRITICAL})
            level = levelmap[levelstr]
            if level is None:
                logger.warning("Unknown logging level '{}', using warning".format(levelstr))
                level = logging.WARNING
        else:
            logger.warning("Event didn't have a level parameter, using warning")
            level = logging.WARNING
        logger.log(level, msg)
