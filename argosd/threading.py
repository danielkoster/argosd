import threading
import logging
from abc import ABCMeta, abstractmethod


class Threaded(metaclass=ABCMeta):

    _stop = None
    _thread = None

    def __init__(self):
        self._stop = threading.Event()
        self._thread = threading.Thread(name=self.get_name(),
                                        target=self.deferred)

    def get_name(self):
        return self.__class__.__name__

    def run(self):
        self._thread.start()

    def stop(self):
        """Stop the current thread and wait for it to finish"""
        logging.info('{} stopping'.format(self.get_name()))
        self._stop.set()
        self._thread.join()
        logging.info('{} stopped'.format(self.get_name()))

    @abstractmethod
    def deferred(self):
        pass
