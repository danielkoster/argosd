from time import sleep
import logging


class ArgosD:

    def run(self):
        while True:
            logger = logging.getLogger('argosd')
            logger.debug("Running")
            sleep(5)
