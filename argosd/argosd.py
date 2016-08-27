import sys
import logging
from time import sleep
from queue import PriorityQueue

from argosd.scheduling import TaskScheduler, TaskRunner


class ArgosD:

    queue = None
    taskscheduler = None
    taskrunner = None

    def __init__(self):
        self.queue = PriorityQueue()
        self.taskscheduler = TaskScheduler(self.queue)
        self.taskrunner = TaskRunner(self.queue)

    def run(self):
        """Starts all processes"""
        logging.info('ArgosD running')

        self.taskscheduler.run()
        self.taskrunner.run()

        while True:
            try:
                sleep(1)
            except KeyboardInterrupt:
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
