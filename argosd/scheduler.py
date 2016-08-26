import logging
import threading
from time import sleep

from argosd.tasks import IPTorrentsTask


class Scheduler:

    _stop = None
    _queue = None
    _thread = None

    def __init__(self, queue):
        self._stop = threading.Event()
        self._queue = queue
        self._thread = threading.Thread(name='scheduler', target=self._loop)

    def run(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

    def _loop(self):
        while(not self._stop.is_set()):
            logging.debug('Scheduler running')
            task = IPTorrentsTask()
            self._queue.put(item=(task.get_priority(), task))
            sleep(5)
