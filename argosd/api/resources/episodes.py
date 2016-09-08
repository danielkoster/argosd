from flask_restful import Resource
from playhouse.shortcuts import model_to_dict

from argosd.models import Episode


class EpisodesResource(Resource):

    def get(self):
        episodes = Episode.select().where(Episode.is_downloaded == 1)
        return [model_to_dict(episode) for episode in episodes]
