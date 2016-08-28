import sys
import logging
import signal
from queue import PriorityQueue

from peewee import *

from argosd import settings
from argosd.scheduling import TaskScheduler, TaskRunner
from argosd.models import Show, Episode


class ArgosD:
    """Main ArgosD class. Starts all runners."""

    queue = None
    taskscheduler = None
    taskrunner = None

    def __init__(self):
        self.queue = PriorityQueue()
        self.taskscheduler = TaskScheduler(self.queue)
        self.taskrunner = TaskRunner(self.queue)

    def run(self):
        """Starts all processes"""
        logging.info('ArgosD starting')

        self._create_database()

        self.taskscheduler.run()
        self.taskrunner.run()

        # Stop everything when a SIGTERM is received
        signal.signal(signal.SIGTERM, self._handle_signal)

        logging.info('ArgosD running')

        # Wait for a signal. This causes our main thread to remain alive,
        # which is needed to properly process any signals.
        signal.pause()

    def _create_database(self):
        database = SqliteDatabase('{}/argosd.db'.format(settings.ARGOSD_PATH))
        database.connect()
        database.create_table(Show, safe=True)
        database.create_table(Episode, safe=True)
        database.close()

    def _handle_signal(self, _signum, _frame):
        self.stop()

    def stop(self):
        """Stops all running processes"""
        logging.info('ArgosD stopping')

        # Tell the scheduler to stop
        logging.info('Telling taskscheduler to stop')
        self.taskscheduler.stop()

        # Tell the taskrunner to stop
        logging.info('Telling taskrunner to stop')
        self.taskrunner.stop()

        logging.info('ArgosD stopped')
        sys.exit(0)
