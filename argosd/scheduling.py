import logging
import threading
from time import sleep
from queue import Empty

from argosd.tasks import IPTorrentsTask


class TaskScheduler:

    _stop = None
    _queue = None
    _thread = None

    def __init__(self, queue):
        self._stop = threading.Event()
        self._queue = queue
        self._thread = threading.Thread(name='taskscheduler', target=self._loop)

    def run(self):
        self._thread.start()

    def stop(self):
        """Stop the TaskScheduler and wait for it to finish"""
        logging.info('TaskScheduler stopping')
        self._stop.set()
        self._thread.join()
        logging.info('TaskScheduler stopped')

    def _loop(self):
        while(not self._stop.is_set()):
            logging.debug('TaskScheduler running')
            task = IPTorrentsTask()
            self._queue.put(item=(task.get_priority(), task))
            sleep(5)


class TaskRunner:

    _stop = None
    _queue = None
    _thread = None

    def __init__(self, queue):
        self._stop = threading.Event()
        self._queue = queue
        self._thread = threading.Thread(name='taskrunner', target=self._loop)

    def run(self):
        self._thread.start()

    def stop(self):
        """Stop the TaskRunner and wait for it to finish"""
        logging.info('TaskRunner stopping')
        self._stop.set()
        self._thread.join()
        logging.info('TaskRunner stopped')

    def _loop(self):
        while(not self._stop.is_set()):
            logging.debug('TaskRunner running')

            try:
                __, task = self._queue.get(block=False)
                task.run()
            except Empty:
                pass

            # Wait at least 1 second before processing a new task
            sleep(1)
