import unittest
from unittest.mock import patch

from argosd.torrentclient import TorrentAlreadyDownloadedException
from tests.dataproviders.torrentclient import TransmissionAlreadyDownloaded


class TransmissionAlreadyDownloadedTestCase(unittest.TestCase):

    @patch('argosd.tasks.Transmission',
           new_callable=TransmissionAlreadyDownloaded)
    def test_download_torrent_raises_exception(self, torrent):
        with self.assertRaises(TorrentAlreadyDownloadedException):
            torrent.download_torrent('test')
