"""This module contains functionality related to multiprocessing.

Multiprocessed: wrapper to easily let classes run in a separate process.
"""
import logging
from multiprocessing import Process
from abc import ABCMeta, abstractmethod


class Multiprocessed(metaclass=ABCMeta):
    """Abstract class used to make a class run in an own process."""

    _process = None

    def __init__(self):
        self._process = Process(name=self.get_name(), target=self.deferred)

    def get_name(self):
        """Returns the name of the current class."""
        return self.__class__.__name__

    def run(self):
        """Starts the process."""
        logging.debug('%s starting', self.get_name())
        self._process.start()
        logging.debug('%s started', self.get_name())

    def stop(self):
        """Stop the current process and wait for it to finish."""
        logging.debug('%s stopping', self.get_name())
        self._stop()
        self._process.terminate()
        self._process.join()
        logging.debug('%s stopped', self.get_name())

    def _stop(self):
        """Used to execute custom commands on shutdown."""
        pass

    @abstractmethod
    def deferred(self):
        """The method being called when the process starts."""
        raise NotImplementedError
