import logging
from time import sleep
from queue import Empty

import schedule

from argosd.tasks import RSSFeedParserTask, EpisodeDownloadTask
from argosd.threading import Threaded


class TaskScheduler(Threaded):
    """Periodically adds tasks to the queue."""

    _queue = None

    def __init__(self, queue):
        super().__init__()
        self._queue = queue

    def deferred(self):
        """Called from the thread, schedules pending tasks."""
        self._create_schedules()

        while not self._stop_event.is_set():
            schedule.run_pending()
            sleep(1)

    def _create_schedules(self):
        schedule.every(10).minutes.do(self._add_rssfeedparsertask)
        schedule.every().minute.do(self._add_episodedownloadtask)

        # Add the RSSFeedParserTask immediately so we don't waste 10 minutes
        self._add_rssfeedparsertask()

    def _add_to_queue(self, task):
        self._queue.put(item=(task.priority, task))

    def _add_rssfeedparsertask(self):
        self._add_to_queue(RSSFeedParserTask())

    def _add_episodedownloadtask(self):
        self._add_to_queue(EpisodeDownloadTask())


class TaskRunner(Threaded):
    """Runs tasks found in the queue."""

    _queue = None

    def __init__(self, queue):
        super().__init__()
        self._queue = queue

    def deferred(self):
        """Called from the thread, runs queued tasks."""
        while not self._stop_event.is_set():
            task = self._get_task_from_queue()

            # Only run a task if we found one
            if task is not None:
                task.run()

            # Wait at least 1 second before processing a new task
            sleep(1)

    def _get_task_from_queue(self):
        """Tries to retrieve a task from the queue."""
        try:
            # Don't block when retrieving tasks from the queue.
            # If we block, the thread stop event isn't processed.
            _, task = self._queue.get(block=False)
            logging.debug('Task found: %s', task.__class__.__name__)
            return task
        except Empty:
            return None
