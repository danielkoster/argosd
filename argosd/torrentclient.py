from abc import ABCMeta, abstractmethod

import transmissionrpc

from argosd import settings


class TorrentClientException(Exception):
    """Exception raised when connection errors occur."""
    pass


class TorrentClient(metaclass=ABCMeta):
    """Abastract class for a torrentclient."""

    @abstractmethod
    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client."""
        raise NotImplementedError


class Transmission(TorrentClient):
    """Connects with a Transmission server."""

    _client = None

    def __init__(self):
        self._client = transmissionrpc.Client(
            address=settings.TRANSMISSION_HOST,
            port=settings.TRANSMISSION_PORT,
            user=settings.TRANSMISSION_USERNAME,
            password=settings.TRANSMISSION_PASSWORD)

    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client."""
        torrent = self._client.add_torrent(torrent_link)
        if not torrent:
            message = 'Could not add torrent "{}" to Transmission' \
                .format(torrent_link)
            raise TorrentClientException(message)
