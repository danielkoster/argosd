import sys
import logging
from time import sleep

from argosd.iptorrents import IPTorrents


class ArgosD:

    _logger = None

    def __init__(self):
        self._logger = logging.getLogger('argosd')

    def run(self):
        """Checks for new series every 10 minutes"""
        self._logger.info('ArgosD running')

        while True:
            try:
                self._check_series()

                # Run every 10 minutes
                sleep(10 * 60)
            except KeyboardInterrupt:
                self._logger.info(
                    'ArgosD stopping, received KeyboardInterrupt')
                sys.exit(0)

    def _check_series(self):
        iptorrents = IPTorrents()
        series = iptorrents.get_series()
        self._logger.debug('Series found: {}'.format(len(series)))
