from flask_restful import Resource
from playhouse.shortcuts import model_to_dict

from argosd.models import Episode
from argosd.api.common.authentication import requires_authentication


class EpisodesResource(Resource):
    """Handles API requests to the /episodes endpoint."""

    @requires_authentication
    def get(self):
        """Handles GET requests. Returns a list of downloaded episodes."""
        episodes = Episode.select().where(Episode.is_downloaded == 1)
        return [model_to_dict(episode) for episode in episodes]
