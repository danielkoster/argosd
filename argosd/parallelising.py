"""This module contains functionality related to parallelising.

Parallelised: abstract wrapper for Threaded and Multiprocessed.
Threaded: wrapper to easily let classes run in a separate thtread.
Multiprocessed: wrapper to easily let classes run in a separate process.
"""
import logging
from threading import Event, Thread
from multiprocessing import Process
from abc import ABCMeta, abstractmethod


class Parallelised(metaclass=ABCMeta):
    """Abstract class to facilitate running jobs in parallel."""

    _paralleled_instance = None
    _stop_event = None

    def run(self):
        """Starts the parallelised job."""
        logging.debug('%s starting', self.__class__.__name__)
        self._paralleled_instance.start()
        logging.debug('%s started', self.__class__.__name__)

    def stop(self):
        """Stop the current parallelised job and wait for it to finish."""
        logging.debug('%s stopping', self.__class__.__name__)
        self.before_stop()
        self._stop_parallelised_instance()
        self._paralleded_instance.join()
        logging.debug('%s stopped', self.__class__.__name__)

    def before_stop(self):
        """Used to execute custom commands on shutdown."""
        pass

    @abstractmethod
    def _stop_parallelised_instance(self):
        raise NotImplementedError

    def _in_parallelised(self):
        """Called when a parallelised job starts, every exception is logged."""
        try:
            self.deferred()
        except Exception as e:
            logging.critical('Exception in %s: %s', self.__class__.__name__, e)

        logging.debug('%s stopped', self.__class__.__name__)

    @abstractmethod
    def deferred(self):
        """The method being called after a parallelised job started."""
        raise NotImplementedError


class Threaded(Parallelised, metaclass=ABCMeta):
    """Abstract class used to make a class run in an own thread."""

    _stop_event = None

    def __init__(self):
        self._stop_event = Event()
        self._paralleled_instance = Thread(name=self.__class__.__name__,
                                           target=self._in_parallelised)

    def _stop_parallelised_instance(self):
        self._stop_event.set()

    @abstractmethod
    def deferred(self):
        """The method being called after a thread started."""
        raise NotImplementedError


class Multiprocessed(Parallelised, metaclass=ABCMeta):
    """Abstract class used to make a class run in an own process."""

    def __init__(self):
        self._paralleled_instance = Process(name=self.__class__.__name__,
                                            target=self._in_parallelised)

    def _stop_parallelised_instance(self):
        self._paralleled_instance.terminate()

    @abstractmethod
    def deferred(self):
        """The method being called after a process started."""
        raise NotImplementedError
