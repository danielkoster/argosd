import logging
from multiprocessing import Process

import flask_restful
from flask import Flask

from argosd import settings
from argosd.api.resources.shows import ShowsResource, ShowResource
from argosd.api.resources.episodes import EpisodesResource


class Api:
    """Creates a RESTful API."""

    _process = None

    def __init__(self):
        self._process = Process(name='Api', target=self.deferred)

    def run(self):
        """Starts the API in it's own process."""
        logging.debug('API starting')
        self._process.start()
        logging.debug('API started')

    def stop(self):
        """Stops the API and waits for it to finish."""
        logging.debug('API stopping')
        self._process.terminate()
        self._process.join()
        logging.debug('API stopped')

    def deferred(self):
        """Runs the API, listens to external requests."""
        # Remove all log handlers set in the main process
        app = Flask('argosd')
        api = flask_restful.Api(app)

        api.add_resource(ShowsResource, '/shows')
        api.add_resource(ShowResource, '/shows/<int:show_id>')
        api.add_resource(EpisodesResource, '/episodes')

        logfile = '{}/api.log'.format(settings.LOG_PATH)
        logformat = '%(message)s'

        logging.basicConfig(format=logformat, level=logging.INFO,
                            filename=logfile, filemode='a')

        app.run(host='0.0.0.0', port=27467)
