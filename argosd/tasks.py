import logging
from abc import ABCMeta, abstractmethod

from argosd.iptorrents import IPTorrents


class BaseTask(metaclass=ABCMeta):
    """Abstract task, provides basic task functionality"""

    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3

    priority = PRIORITY_NORMAL

    @abstractmethod
    def run(self):
        """Method called when task is run"""
        pass

    def get_priority(self):
        """Returns the priority of this task"""
        return self.priority


class IPTorrentsTask(BaseTask):
    """Task to retrieve and download torrents from IPTorrents"""

    def run(self):
        iptorrents = IPTorrents()
        series = iptorrents.get_series()
        logging.debug('Series found: %d', len(series))
