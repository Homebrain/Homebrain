from homebrain import Agent, Dispatcher, Event
import logging


class LogListener(Agent):

    autostart = True

    def __init__(self, target=None):
        super(LogListener, self).__init__()
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.unknown_logger = logging.getLogger("Unknown Client")
        Dispatcher().bind(self, "log")

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
        levelstr = data["level"].lower()
        if "level" in data:
            levelmap = {"debug": logging.DEBUG,
                        "info": logging.INFO,
                        "warning": logging.WARNING,
                        "error": logging.ERROR,
                        "critical": logging.CRITICAL}
            if levelstr in levelmap:
                level = levelmap[levelstr]
            else:
                logger.warning("Unknown logging level '{}', using warning".format(levelstr))
                level = logging.WARNING
        else:
            logger.warning("Event didn't have a level parameter, using warning")
            level = logging.WARNING
        logger.log(level, msg)
        Dispatcher().put_event(Event(type="logmsg", data={"level": levelstr, "msg": msg}))
