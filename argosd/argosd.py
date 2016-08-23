from time import sleep
from daemonize import Daemonize
import logging

pid = "/var/run/argosd.pid"

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

logfile_handler = logging.FileHandler("/var/log/argosd.log", "w")
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
logger.addHandler(logfile_handler)

keep_fds = [logfile_handler.stream.fileno()]


def main():
    while True:
        logger.debug("Running")
        sleep(5)

daemon = Daemonize(app="argosd", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
