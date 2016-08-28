import sys
import logging
import signal
from queue import PriorityQueue

from argosd.scheduling import TaskScheduler, TaskRunner


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
        self.taskscheduler.run()
        self.taskrunner.run()

        # Stop everything when a SIGTERM is received
        signal.signal(signal.SIGTERM, self._handle_signal)

        logging.info('ArgosD running')

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
