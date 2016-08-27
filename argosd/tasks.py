import logging
from abc import ABCMeta, abstractmethod

from argosd.iptorrents import IPTorrents


class BaseTask(metaclass=ABCMeta):

    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_priority(self):
        pass

    def __lt__(self, other):
        """Makes tasks comparable with each other"""
        return self.get_priority() - other.get_priority()


class IPTorrentsTask(BaseTask):

    def run(self):
        iptorrents = IPTorrents()
        series = iptorrents.get_series()
        logging.debug('Series found: {}'.format(len(series)))

    def get_priority(self):
        return self.PRIORITY_NORMAL
