import logging
from multiprocessing import Process

import flask_restful
from flask import Flask

from argosd import settings
from argosd.api.resources.shows import ShowsResource, ShowResource
from argosd.api.resources.episodes import EpisodesResource


class Api:

    _app = None
    _api = None
    _process = None

    def __init__(self):
        self._app = Flask('argosd')

        self._api = flask_restful.Api(self._app)

        self._api.add_resource(ShowsResource, '/shows')
        self._api.add_resource(ShowResource, '/shows/<int:show_id>')
        self._api.add_resource(EpisodesResource, '/episodes')

        self._process = Process(name='Api', target=self.deferred)

    def run(self):
        logging.debug('API starting')
        self._process.start()
        logging.debug('API started')

    def stop(self):
        logging.debug('API stopping')
        self._process.terminate()
        self._process.join()
        logging.debug('API stopped')

    def deferred(self):
        """Starts the API, listens to external requests"""
        # Remove all log handlers set in the main process
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logfile = '{}/api.log'.format(settings.LOG_PATH)
        logformat = '%(message)s'

        logging.basicConfig(format=logformat, level=logging.INFO,
                            filename=logfile, filemode='a')

        self._app.run(host='0.0.0.0', port=27467)
