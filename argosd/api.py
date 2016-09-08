import logging
from multiprocessing import Process

import flask_restful
from flask import Flask
from flask_restful import reqparse, abort, Resource
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict

from argosd import settings
from argosd.threading import Threaded
from argosd.models import Show, Episode


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


class ShowsResource(Resource):

    def get(self):
        shows = Show.select()
        return [model_to_dict(show) for show in shows]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('follow_from_season', type=int, required=True)
        parser.add_argument('follow_from_episode', type=int, required=True)
        parser.add_argument('quality_threshold', type=int, required=True)
        parser.add_argument('wait_minutes_for_better_quality', type=int)
        args = parser.parse_args()

        show = Show()
        show.title = args['title']
        show.follow_from_season = args['follow_from_season']
        show.follow_from_episode = args['follow_from_episode']
        show.quality_threshold = args['quality_threshold']

        if args['wait_minutes_for_better_quality']:
            show.wait_minutes_for_better_quality = \
                args['wait_minutes_for_better_quality']

        try:
            show.save()
        except IntegrityError as e:
            abort(400, message=str(e))

        return model_to_dict(show), 201


class ShowResource(Resource):

    def get(self, show_id):
        try:
            show = Show.get(Show.id == show_id)
            return model_to_dict(show)
        except DoesNotExist:
            abort(404)

    def delete(self, show_id):
        try:
            show = Show.get(Show.id == show_id)
            show.delete_instance()
            return '', 204
        except DoesNotExist:
            abort(404)

    def put(self, show_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('follow_from_season', type=int, required=True)
        parser.add_argument('follow_from_episode', type=int, required=True)
        parser.add_argument('quality_threshold', type=int, required=True)
        parser.add_argument('wait_minutes_for_better_quality', type=int)
        args = parser.parse_args()

        try:
            show = Show.get(Show.id == show_id)
        except DoesNotExist:
            abort(404)

        show.title = args['title']
        show.follow_from_season = args['follow_from_season']
        show.follow_from_episode = args['follow_from_episode']
        show.quality_threshold = args['quality_threshold']

        if args['wait_minutes_for_better_quality']:
            show.wait_minutes_for_better_quality = \
                args['wait_minutes_for_better_quality']

        try:
            show.save()
        except IntegrityError as e:
            abort(400, message=str(e))

        return model_to_dict(show), 201


class EpisodesResource(Resource):

    def get(self):
        episodes = Episode.select()
        return [model_to_dict(episode) for episode in episodes]
