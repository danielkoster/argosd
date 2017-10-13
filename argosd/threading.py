import threading
import logging
from abc import ABCMeta, abstractmethod


class Threaded(metaclass=ABCMeta):
    """Abstract class used to make a class run in an own thread."""

    _stop_event = None
    _thread = None

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(name=self.get_name(),
                                        target=self.deferred)

    def get_name(self):
        """Returns the name of the current class."""
        return self.__class__.__name__

    def run(self):
        """Starts the thread."""
        logging.debug('%s starting', self.get_name())
        self._thread.start()
        logging.debug('%s started', self.get_name())

    def stop(self):
        """Stop the current thread and wait for it to finish."""
        logging.debug('%s stopping', self.get_name())
        self._stop_event.set()
        self._stop()
        self._thread.join()
        logging.debug('%s stopped', self.get_name())

    def _stop(self):
        """Used to execute custom commands on shutdown."""
        pass

    @abstractmethod
    def deferred(self):
        """The method being called when the thread starts."""
        raise NotImplementedError
