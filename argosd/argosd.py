from argosd import iptorrents
from time import sleep
import logging
import sys


class ArgosD:

    def run(self):
        self.logger = logging.getLogger('argosd')
        self.logger.info('ArgosD running')

        while True:
            try:
                self._check_series()

                # Run every 10 minutes
                sleep(10 * 60)
            except KeyboardInterrupt:
                self.logger.info('ArgosD stopping, received KeyboardInterrupt')
                sys.exit(0)

    def _check_series(self):
        ipt = iptorrents.IPTorrents()
        series = ipt.get_series()
        self.logger.debug('Series found: {}'.format(len(series)))
