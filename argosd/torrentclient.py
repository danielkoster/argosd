from abc import ABCMeta, abstractmethod

import transmissionrpc

from argosd import settings


class TorrentClientException(Exception):
    """Exception raised when connection errors occur."""
    pass


class TorrentAlreadyDownloadedException(Exception):
    """Exception raised when a torrent is added to a torrentclient,
    but the torrentclient already has downloaded it."""
    pass


class TorrentClient(metaclass=ABCMeta):
    """Abastract class for a torrentclient."""

    @abstractmethod
    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client."""
        raise NotImplementedError

    @staticmethod
    def raise_exception(message):
        """Shorthand to raise a TorrentClientException.
        All exceptions should be converted to this type
        so they can be handled outside of this scope."""
        raise TorrentClientException(message)


class Transmission(TorrentClient):
    """Connects with a Transmission server."""

    _client = None

    def __init__(self):
        try:
            self._client = transmissionrpc.Client(
                address=settings.TRANSMISSION_HOST,
                port=settings.TRANSMISSION_PORT,
                user=settings.TRANSMISSION_USERNAME,
                password=settings.TRANSMISSION_PASSWORD)
        except transmissionrpc.TransmissionError as e:
            self.raise_exception(str(e))

    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client."""
        try:
            torrent = self._client.add_torrent(torrent_link)
            if not torrent:
                message = 'Could not add torrent "{}" to Transmission' \
                    .format(torrent_link)
                raise TorrentClientException(message)
        except transmissionrpc.TransmissionError as e:
            if e.message == 'Query failed with result "duplicate torrent".':
                raise TorrentAlreadyDownloadedException()

            self.raise_exception(str(e))
