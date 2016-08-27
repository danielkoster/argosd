import logging
from time import sleep
from queue import Empty

import schedule

from argosd.tasks import IPTorrentsTask
from argosd.threading import Threaded


class TaskScheduler(Threaded):

    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super().__init__()

        self._create_schedules()

    def deferred(self):
        """Called from the thread, schedules pending tasks"""
        while(not self._stop.is_set()):
            schedule.run_pending()
            sleep(1)

    def _create_schedules(self):
        schedule.every(5).seconds.do(self._add_to_queue, IPTorrentsTask)

    def _add_to_queue(self, task_class):
        # Create a new instance of the given class
        task = task_class()
        self._queue.put(item=(task.get_priority(), task))


class TaskRunner(Threaded):

    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super().__init__()

    def deferred(self):
        """Called from the thread, runs queued tasks"""
        while(not self._stop.is_set()):
            try:
                __, task = self._queue.get(block=False)
                logging.debug('Task found: {}'.format(task.__class__.__name__))
                task.run()
            except Empty:
                pass

            # Wait at least 1 second before processing a new task
            sleep(1)
