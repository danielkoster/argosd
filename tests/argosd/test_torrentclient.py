import unittest
from unittest.mock import patch

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
    def test_download_dir(self):
        show = self._get_new_dummy_show()
        episode = self._get_new_dummy_episode(show)

        client = Transmission()
        download_dir = client._get_download_dir(episode)
        self.assertEqual(download_dir, '/tmp/test.show')
