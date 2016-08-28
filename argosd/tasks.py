import logging
from abc import ABCMeta, abstractmethod

from argosd.iptorrents import IPTorrents


class BaseTask(metaclass=ABCMeta):

    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3

    priority = PRIORITY_NORMAL

    @abstractmethod
    def run(self):
        pass

    def get_priority(self):
        return self.priority


class IPTorrentsTask(BaseTask):

    def run(self):
        iptorrents = IPTorrents()
        series = iptorrents.get_series()
        logging.debug('Series found: {}'.format(len(series)))
