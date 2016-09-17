from flask_restful import Resource

from argosd.models import Episode
from argosd.api.common.authentication import requires_authentication


class EpisodesResource(Resource):
    """Handles API requests to the /episodes endpoint."""

    @staticmethod
    @requires_authentication
    def get():
        """Handles GET requests. Returns a list of downloaded episodes."""
        episodes = Episode.select().where(Episode.is_downloaded == 1)
        return [episode.to_dict() for episode in episodes]
