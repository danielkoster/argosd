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
        schedule.every(5).seconds.do(self._add_iptorrentstask)

    def _add_to_queue(self, task):
        self._queue.put(item=(task.get_priority(), task))

    def _add_iptorrentstask(self):
        self._add_to_queue(IPTorrentsTask())


class TaskRunner(Threaded):

    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super().__init__()

    def deferred(self):
        """Called from the thread, runs queued tasks"""
        while(not self._stop.is_set()):
            task = self._get_task_from_queue()
            task.run()

            # Wait at least 1 second before processing a new task
            sleep(1)

    def _get_task_from_queue(self):
        try:
            # Don't block when retrieving tasks from the queue
            # If we block, the thread stop event isn't processed
            __, task = self._queue.get(block=False)
            logging.debug('Task found: {}'.format(task.__class__.__name__))
            return task
        except Empty:
            pass
