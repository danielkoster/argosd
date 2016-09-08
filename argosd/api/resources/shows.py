from flask_restful import reqparse, abort, Resource
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist, IntegrityError

from argosd.models import Show


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('follow_from_season', type=int, required=True)
parser.add_argument('follow_from_episode', type=int, required=True)
parser.add_argument('quality_threshold', type=int, required=True)
parser.add_argument('wait_minutes_for_better_quality', type=int)


class ShowsResource(Resource):

    def get(self):
        shows = Show.select()
        return [model_to_dict(show) for show in shows]

    def post(self):
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
