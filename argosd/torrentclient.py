from abc import ABCMeta, abstractmethod

import transmissionrpc

from argosd import settings


class TorrentClientException(Exception):
    """Generic exception thrown when an issue in connectivity with the
       torrentclient occurs.
       All exceptions should be converted to this type
       so they can be handled outside of this scope."""
    pass


class TorrentClient(metaclass=ABCMeta):
    """Abastract class for a torrentclient."""

    @abstractmethod
    def download_episode(self, episode):
        """Add the torrent from the episode to a torrent client."""
        raise NotImplementedError


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
            raise TorrentClientException(str(e))

    def download_episode(self, episode):
        """Add the torrent from the episode to a torrent client."""
        try:
            path = self._get_download_dir(episode)
            torrent = self._client.add_torrent(episode.link, download_dir=path)
            if torrent:
                logging.info('Downloaded episode: %s', episode)
            else:
                message = 'Could not add torrent "{}" to Transmission' \
                    .format(episode.link)
                raise TorrentClientException(message)
        except transmissionrpc.TransmissionError as e:
            # Silently continue when episode is already downloaded
            if e.message == 'Query failed with result "duplicate torrent".':
                logging.info('Already downloaded episode %s', episode)

            raise TorrentClientException(str(e))

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
                raise TorrentClientException(str(e))

        path_suffix = episode.show.title.lower().replace(' ', '.')
        return "{}/{}".format(path_prefix, path_suffix)
