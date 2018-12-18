from abc import ABCMeta, abstractmethod
import os
import tempfile

import logging
import requests
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

    DOWNLOAD_STRUCTURE_DEFAULT = 1
    DOWNLOAD_STRUCTURE_PLEX = 2

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

            # Download the torrent to a temporary file
            tmpfile = tempfile.NamedTemporaryFile(suffix='.torrent')
            r = requests.get(episode.link, allow_redirects=True)
            tmpfile.write(r.content)

            # Allow the transmission-daemon user to read the file
            os.chmod(tmpfile.name, 0o666)

            torrent = self._client.add_torrent(tmpfile.name, download_dir=path)

            # Delete the file
            tmpfile.close()

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

        # Determine path suffix based on desired strategy
        if settings.DOWNLOAD_STRUCTURE_STRATEGY == \
                self.DOWNLOAD_STRUCTURE_DEFAULT:
            path_suffix = episode.show.title.lower().replace(' ', '.')
        elif settings.DOWNLOAD_STRUCTURE_STRATEGY == \
                self.DOWNLOAD_STRUCTURE_PLEX:
            # Add leading zero, if needed
            season = str(episode.season).zfill(2)
            path_suffix = '{}/Season {}'.format(episode.show.title, season)
        else:
            message = 'No download structure strategy is defined'
            raise TorrentClientException(message)

        return "{}/{}".format(path_prefix, path_suffix)
