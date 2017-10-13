import logging
from multiprocessing import Process

import flask_restful
from flask import Flask

from argosd import settings
from argosd.multiprocessing import Multiprocessed
from argosd.api.resources.shows import ShowsResource, ShowResource
from argosd.api.resources.episodes import EpisodesResource


class Api(Multiprocessed):
    """Creates a RESTful API."""

    def deferred(self):
        """Runs the API, listens to external requests."""
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
