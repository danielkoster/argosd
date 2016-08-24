from time import sleep
import logging

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

logfile_handler = logging.FileHandler("/var/log/argosd/argosd.log", "w")
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logfile_handler)

logger.info("ArgosD starting")

while True:
    logger.debug("Running")
    sleep(5)
