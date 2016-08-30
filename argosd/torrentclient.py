import logging
from abc import ABCMeta, abstractmethod

import transmissionrpc

from argosd import settings


class TorrentClientException(Exception):
    pass


class TorrentClient(metaclass=ABCMeta):

    @abstractmethod
    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client"""
        pass


class Transmission(TorrentClient):

    _client = None

    def __init__(self):
        self._client = transmissionrpc.Client(
            address=settings.TRANSMISSION_HOST,
            port=settings.TRANSMISSION_PORT,
            user=settings.TRANSMISSION_USERNAME,
            password=settings.TRANSMISSION_PASSWORD)

    def download_torrent(self, torrent_link):
        """Add a torrent file from a URL to the client"""
        torrent = self._client.add_torrent(torrent_link)
        if not torrent:
            message = 'Could not add torrent "{}" to Transmission' \
                .format(torrent_link)
            raise TorrentClientException(message)

    def get_download_dir(self):
        return self._client.session_stats().download_dir

    def get_download_dir_free_space(self):
        return self._client.session_stats().download_dir_free_space
