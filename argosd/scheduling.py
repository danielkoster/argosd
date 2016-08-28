import logging
from time import sleep
from queue import Empty

import schedule

from argosd.tasks import RSSFeedParserTask
from argosd.threading import Threaded


class TaskScheduler(Threaded):
    """Adds tasks to the queue"""

    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super().__init__()

        self._create_schedules()

    def deferred(self):
        """Called from the thread, schedules pending tasks"""
        while not self._stop.is_set():
            schedule.run_pending()
            sleep(1)

    def _create_schedules(self):
        schedule.every(30).seconds.do(self._add_rssfeedparserstask)

    def _add_to_queue(self, task):
        self._queue.put(item=(task.priority, task))

    def _add_rssfeedparserstask(self):
        self._add_to_queue(RSSFeedParserTask())


class TaskRunner(Threaded):
    """Runs tasks found in the queue"""

    _queue = None

    def __init__(self, queue):
        self._queue = queue
        super().__init__()

    def deferred(self):
        """Called from the thread, runs queued tasks"""
        while not self._stop.is_set():
            task = self._get_task_from_queue()

            # Only run a task if we found one
            if task is not None:
                task.run()

            # Wait at least 1 second before processing a new task
            sleep(1)

    def _get_task_from_queue(self):
        """Tries to retrieve a task from the queue"""
        try:
            # Don't block when retrieving tasks from the queue
            # If we block, the thread stop event isn't processed
            _, task = self._queue.get(block=False)
            logging.debug('Task found: %s', task.__class__.__name__)
            return task
        except Empty:
            return None
