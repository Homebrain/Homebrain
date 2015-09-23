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
            if levelstr == "debug":
                level = logging.DEBUG
            elif levelstr == "info":
                level = logging.INFO
            elif levelstr == "warning":
                level = logging.WARNING
            elif levelstr == "critical":
                level = logging.CRITICAL
            else:
                self.log("Unknown logging level " + levelstr)
                level = logging.INFO
        else:
            level = logging.INFO
        logger.log(level, msg)
