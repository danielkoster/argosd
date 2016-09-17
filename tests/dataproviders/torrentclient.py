from unittest.mock import MagicMock

from argosd.torrentclient import TorrentClient, \
    TorrentAlreadyDownloadedException


class TransmissionAlreadyDownloaded(MagicMock):

    def download_torrent(self, link):
        raise TorrentAlreadyDownloadedException()
