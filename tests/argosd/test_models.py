import unittest
from unittest.mock import patch

from peewee import SqliteDatabase
from playhouse.test_utils import test_database

from argosd.models import Show, Episode
from tests.dataproviders.torrentclient import TransmissionAlreadyDownloaded

database = SqliteDatabase('argosd_test.db')


class EpisodeTestCase(unittest.TestCase):

    def _get_new_dummy_show(self):
        show = Show()
        show.title = 'testshow'
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

    @patch('argosd.models.Transmission',
           new_callable=TransmissionAlreadyDownloaded)
    def test_download_already_downloaded_episode(self, transmission):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            episode = self._get_new_dummy_episode(show)
            episode.save()

            self.assertFalse(episode.is_downloaded)

            episode.download()

            episode = Episode.get()
            self.assertTrue(episode.is_downloaded)
