import logging
import time
import os
from .core import Event
from .utils import get_cwd
from .dispatcher import Dispatcher

logformat = "%(asctime)s %(levelname)s from %(threadName)s: %(message)s"
formatter = logging.Formatter(logformat)

def setup_logging(debug=False):
    # Log level
    loglevel = logging.DEBUG if debug else logging.INFO
    # Log format
    logging.basicConfig(level=loglevel, format=logformat)
    # Event logger for logmsg events so WebUI and other remote apps can see them
    eventlogger = EventLogHandler()
    logging.getLogger().addHandler(eventlogger)
    # Logging to file
    filelogger = FileLogHandler()
    logging.getLogger().addHandler(filelogger)


class EventLogHandler(logging.Handler):
    def __init__(self, debug=False):
        logging.Handler.__init__(self)

    def flush(self):
        pass

    def handle(self, record):
        event = {"tag": "logmsg",
                 "data": {
                     "level": record.levelname.lower(),
                     "msg": record.getMessage()
                }}
        Dispatcher().put_event(Event(tag="logmsg", data=event["data"]))

class FileLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.logfolder = get_cwd()+"/logs/"
        try:
            os.mkdir(self.logfolder)
        except FileExistsError:
            pass
        self.logfilename = self.logfolder+time.strftime("%Y-%m-%d %Hh-%Mm")+".log"
        logging.info("Logging to: " + self.logfilename)
        self.logfile = open(self.logfilename, 'a')

    def flush(self):
        pass

    def handle(self, record):
        logstr = formatter.format(record) + "\n"
        self.logfile.write(logstr)
        self.logfile.flush()
