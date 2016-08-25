import sys
import logging
from time import sleep

from argosd.iptorrents import IPTorrents


class ArgosD:

    def run(self):
        """Checks for new series every 10 minutes"""
        logging.info('ArgosD running')

        while True:
            try:
                self._check_series()

                # Run every 10 minutes
                sleep(10 * 60)
            except KeyboardInterrupt:
                logging.info(
                    'ArgosD stopping, received KeyboardInterrupt')
                sys.exit(0)

    def _check_series(self):
        iptorrents = IPTorrents()
        series = iptorrents.get_series()
        logging.debug('Series found: {}'.format(len(series)))
