import sys
import logging
import signal
from queue import PriorityQueue

from peewee import *

from argosd import settings
from argosd.scheduling import TaskScheduler, TaskRunner
from argosd.models import Show, Episode
from argosd.bots import TelegramBot
from argosd.api.app import Api


class ArgosD:
    """Main ArgosD class. Starts all runners and processes."""

    taskscheduler = None
    taskrunner = None
    api = None
    bot = None

    def __init__(self):
        queue = PriorityQueue()
        self.taskscheduler = TaskScheduler(queue)
        self.taskrunner = TaskRunner(queue)
        self.api = Api()

        if settings.TELEGRAM_BOT_TOKEN:
            self.bot = TelegramBot()

    def run(self):
        """Starts all runners and processes."""
        logging.info('ArgosD starting')

        self._create_database()

        logging.info('Starting taskscheduler')
        self.taskscheduler.run()

        logging.info('Starting taskrunner')
        self.taskrunner.run()

        logging.info('Starting API')
        self.api.run()

        if settings.TELEGRAM_BOT_TOKEN:
            logging.info('Starting telegrambot')
            self.bot.run()

        # Stop everything when a SIGTERM is received
        signal.signal(signal.SIGTERM, self._handle_signal)

        logging.info('ArgosD running')

        # Wait for a signal. This causes our main thread to remain alive,
        # which is needed to properly process any signals.
        signal.pause()

    @staticmethod
    def _create_database():
        database = SqliteDatabase('{}/argosd.db'.format(settings.ARGOSD_PATH))
        database.connect()
        database.create_tables([Show, Episode], safe=True)
        database.close()

    def _handle_signal(self, signum, frame):
        del frame  # Unused

        if signum == signal.SIGTERM:
            self.stop()

    def stop(self):
        """Stops all runners and processes."""
        logging.info('ArgosD stopping')

        logging.info('Telling taskscheduler to stop')
        self.taskscheduler.stop()

        logging.info('Telling taskrunner to stop')
        self.taskrunner.stop()

        logging.info('Telling API to stop')
        self.api.stop()

        if settings.TELEGRAM_BOT_TOKEN:
            logging.info('Telling telegrambot to stop')
            self.bot.stop()

        logging.info('ArgosD stopped')
        sys.exit(0)
