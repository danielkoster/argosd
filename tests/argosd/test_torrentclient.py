import unittest
from unittest.mock import Mock, patch

from argosd.torrentclient import Transmission
from argosd.models import Show, Episode


class TransmissionTaskTestCase(unittest.TestCase):

    def _get_new_dummy_show(self):
        show = Show()
        show.title = 'Test show'
        show.follow_from_season = 1
        show.follow_from_episode = 1
        show.minimum_quality = 720
        return show

    def _get_new_dummy_episode(self, show):
        episode = Episode()
        episode.show = show
        episode.link = 'testlink'
        episode.season = 1
        episode.episode = 1
        episode.quality = 720
        return episode

    @patch('argosd.settings.TORRENTCLIENT_DOWNLOAD_DIR', '/tmp')
    @patch('argosd.settings.DOWNLOAD_STRUCTURE_STRATEGY',
           Transmission.DOWNLOAD_STRUCTURE_DEFAULT)
    @patch('transmissionrpc.Client', new_callable=Mock)
    def test_download_dir_default(self, transmissionrpc_client):
        show = self._get_new_dummy_show()
        episode = self._get_new_dummy_episode(show)

        client = Transmission()
        download_dir = client._get_download_dir(episode)
        self.assertEqual(download_dir, '/tmp/test.show')

    @patch('argosd.settings.TORRENTCLIENT_DOWNLOAD_DIR', '/tmp')
    @patch('argosd.settings.DOWNLOAD_STRUCTURE_STRATEGY',
           Transmission.DOWNLOAD_STRUCTURE_PLEX)
    @patch('transmissionrpc.Client', new_callable=Mock)
    def test_download_dir_plex(self, transmissionrpc_client):
        show = self._get_new_dummy_show()
        episode = self._get_new_dummy_episode(show)

        client = Transmission()
        download_dir = client._get_download_dir(episode)
        self.assertEqual(download_dir, '/tmp/Test show/Season 01')
