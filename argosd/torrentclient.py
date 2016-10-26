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
    def download_episode(self, episode):
        """Add a torrent file from an episode to the client."""
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

    def download_episode(self, episode):
        """Add a torrent file from a URL to the client."""
        try:
            path = self._get_download_dir(episode)
            torrent = self._client.add_torrent(episode.link, download_dir=path)
            if not torrent:
                message = 'Could not add torrent "{}" to Transmission' \
                    .format(episode.link)
                raise TorrentClientException(message)
        except transmissionrpc.TransmissionError as e:
            if e.message == 'Query failed with result "duplicate torrent".':
                raise TorrentAlreadyDownloadedException()

            self.raise_exception(str(e))

    def _get_download_dir(self, episode):
        """Returns the path to the location where the torrentclient will
           download files to."""
        # Check for optional override in settings file
        if settings.TORRENTCLIENT_DOWNLOAD_DIR:
            path_prefix = settings.TORRENTCLIENT_DOWNLOAD_DIR
        else:
            try:
                session = transmissionrpc.Session(self._client)
                # Retrieve data from Transmission
                session.update()
                path_prefix = session.download_dir
            except transmissionrpc.TransmissionError as e:
                self.raise_exception(str(e))

        path_suffix = episode.show.title.lower().replace(' ', '.')
        return "{}/{}".format(path_prefix, path_suffix)
