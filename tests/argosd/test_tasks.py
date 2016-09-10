import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from peewee import SqliteDatabase
from playhouse.test_utils import test_database

from argosd.tasks import EpisodeDownloadTask
from argosd.models import Show, Episode

database = SqliteDatabase('argosd_test.db')


class EpisodeDownloadTaskTestCase(unittest.TestCase):

    def _get_new_dummy_show(self):
        show = Show()
        show.title = 'testshow'
        show.follow_from_season = 1
        show.follow_from_episode = 1
        show.quality_threshold = 720
        return show

    def _get_new_dummy_episode(self, show):
        episode = Episode()
        episode.show = show
        episode.link = 'testlink'
        episode.season = 1
        episode.episode = 1
        episode.quality = 720
        return episode

    def test_highest_quality_is_downloaded(self):
        show = self._get_new_dummy_show()

        episode_one = self._get_new_dummy_episode(show)

        episode_two = self._get_new_dummy_episode(show)
        episode_two.quality = 1080

        episodedownloadtask = EpisodeDownloadTask()
        episodedownloadtask._download_episode = MagicMock()
        # _get_episodes always returns highest quality first
        episodedownloadtask._get_episodes = MagicMock(return_value=[
            episode_two, episode_one])
        episodedownloadtask._deferred()

        episodedownloadtask._download_episode.assert_called_once_with(
            episode_two)

    def test_get_episodes_returns_highest_quality_first(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            episode_one = self._get_new_dummy_episode(show)
            episode_one.save()

            episode_two = self._get_new_dummy_episode(show)
            episode_two.quality = 1080
            episode_two.save()

            episodedownloadtask = EpisodeDownloadTask()
            episodes = episodedownloadtask._get_episodes()

            # Second episode has highest quality and should be first
            self.assertEqual(episodes[0].id, episode_two.id)
            self.assertEqual(episodes[1].id, episode_one.id)

    def test_wait_minutes_for_higher_quality_is_followed(self):
        show = self._get_new_dummy_show()
        show.wait_minutes_for_better_quality = 5

        episode = self._get_new_dummy_episode(show)

        episodedownloadtask = EpisodeDownloadTask()
        episodedownloadtask._download_episode = MagicMock()

        episodedownloadtask._get_episodes = MagicMock(return_value=[episode])
        episodedownloadtask._deferred()
        episodedownloadtask._download_episode.call_count = 0

        # It should be downloaded if it was created 10 minutes ago,
        # because it only has to wait for 5 minutes.
        episode.created_at = datetime.now() - timedelta(minutes=10)

        episodedownloadtask._get_episodes = MagicMock(return_value=[episode])
        episodedownloadtask._deferred()
        episodedownloadtask._download_episode.call_count = 1
