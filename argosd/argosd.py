import sys
import logging
from time import sleep
from queue import PriorityQueue

from argosd.scheduler import Scheduler


class ArgosD:

    queue = None
    scheduler = None

    def __init__(self):
        self.queue = PriorityQueue()
        self.scheduler = Scheduler(self.queue)

    def run(self):
        """Starts all processes"""
        logging.info('ArgosD running')

        self.scheduler.run()

        while True:
            try:
                __, task = self.queue.get()
                task.run()

                # Wait at least 1 second before processing a new task
                sleep(1)
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        """Stops all running processes"""
        logging.info('ArgosD stopping')

        # Tell the scheduler to stop and wait for it to finish
        logging.info('Telling scheduler to stop')
        self.scheduler.stop()
        logging.info('Scheduler stopped')

        logging.info('ArgosD stopped')
        sys.exit(0)
