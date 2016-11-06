import logging
from time import sleep
from queue import Empty

import schedule

from argosd.parallelising import Threaded
from argosd.tasks import RSSFeedParserTask, EpisodeDownloadTask


class TaskScheduler(Threaded):
    """Periodically adds tasks to the queue."""

    _queue = None

    def __init__(self, queue):
        super().__init__()
        self._queue = queue

    def deferred(self):
        """Called from the thread, schedules pending tasks."""
        schedule.every(10).minutes.do(self._add_rssfeedparsertask)
        schedule.every().minute.do(self._add_episodedownloadtask)

        # Add the RSSFeedParserTask immediately so we don't waste 10 minutes
        self._add_rssfeedparsertask()

        while not self._stop_event.is_set():
            schedule.run_pending()
            sleep(1)

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
            try:
                # Don't block when retrieving tasks from the queue.
                # If we block, the thread stop event isn't processed.
                _, task = self._queue.get(block=False)
                logging.debug('Task found: %s', task.__class__.__name__)
                task.run()
            except Empty:
                # Try again next iteration.
                pass

            # Wait at least 1 second before processing a new task.
            sleep(1)
