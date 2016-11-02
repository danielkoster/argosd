import unittest
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime, timedelta

from peewee import SqliteDatabase
from playhouse.test_utils import test_database

from argosd.tasks import RSSFeedParserTask, EpisodeDownloadTask
from argosd.models import Show, Episode
from argosd.torrentclient import Transmission
from tests.dataproviders import rss

database = SqliteDatabase('argosd_test.db')


class RSSFeedParserTaskTestCase(unittest.TestCase):

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

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_MATCHING_ITEM)
    def test_follow_from_is_followed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.follow_from_season = 2
            show.follow_from_episode = 2
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 1)
            self.assertEqual(episodes[0].title, 'testshow')

        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.follow_from_season = 3
            show.follow_from_episode = 2
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 0)

        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.follow_from_season = 2
            show.follow_from_episode = 5
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 0)

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_MATCHING_ITEM)
    def test_parse_single_episodes_from_feed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 1)
            self.assertEqual(episodes[0].title, 'testshow')

    @patch('argosd.settings.RSS_FEED', rss.MULTIPLE_MATCHING_ITEMS)
    def test_parse_multiple_full_episodes_from_feed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 3)

            self.assertEqual(episodes[0].title, 'testshow')
            self.assertEqual(episodes[0].season, 2)
            self.assertEqual(episodes[0].episode, 3)
            self.assertEqual(episodes[0].quality, 720)

            self.assertEqual(episodes[1].title, 'testshow')
            self.assertEqual(episodes[1].season, 2)
            self.assertEqual(episodes[1].episode, 3)
            self.assertEqual(episodes[1].quality, 1080)

            self.assertEqual(episodes[2].title, 'testshow')
            self.assertEqual(episodes[2].season, 2)
            self.assertEqual(episodes[2].episode, 3)
            self.assertEqual(episodes[2].quality, 720)

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_ITEM_CAPITALISATION)
    def test_parse_capitalised_episodes_from_feed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 1)
            self.assertEqual(episodes[0].title, 'testshow')

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_ITEM_SPECIAL_CHARS)
    def test_parse_special_chars_episodes_from_feed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.title = 'Mr. Robot'
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 1)
            self.assertEqual(episodes[0].title, 'Mr. Robot')

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_ITEM_LOW_QUALITY)
    def test_parse_low_quality_episodes_from_feed(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            rssfeedparsertask = RSSFeedParserTask()
            episodes = rssfeedparsertask._parse_episodes_from_feed()

            self.assertEqual(len(episodes), 0)

    @patch('argosd.settings.RSS_FEED', rss.SINGLE_MATCHING_ITEM)
    def test_save_already_downloaded_episode(self):
        with test_database(database, (Show, Episode)):
            show = self._get_new_dummy_show()
            show.save()

            episode = self._get_new_dummy_episode(show)
            episode.season = 2
            episode.episode = 3
            episode.quality = 1080
            episode.is_downloaded = True
            episode.save()

            rssfeedparsertask = RSSFeedParserTask()
            rssfeedparsertask._deferred()

            episodes = rssfeedparsertask._parse_episodes_from_feed()
            self.assertEqual(len(episodes), 0)


class EpisodeDownloadTaskTestCase(unittest.TestCase):

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

    def test_highest_quality_is_downloaded(self):
        show = self._get_new_dummy_show()

        episode_one = self._get_new_dummy_episode(show)
        # Don't download episode
        episode_one.download = MagicMock()

        episode_two = self._get_new_dummy_episode(show)
        episode_two.quality = 1080
        # Don't send actual notifications to users and don't download episode
        episode_two._notify_user = MagicMock()
        episode_two.download = MagicMock()

        episodedownloadtask = EpisodeDownloadTask()

        # _get_episodes always returns highest quality first
        episodedownloadtask._get_episodes = MagicMock(return_value=[
            episode_two, episode_one])
        # Don't send actual notifications to users
        episodedownloadtask._notify_user = MagicMock()
        episodedownloadtask._deferred()

        episode_one.download.assert_not_called()

        episodedownloadtask._notify_user.assert_called_once_with(
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

    @patch.object(Episode, 'download')
    def test_wait_minutes_for_higher_quality_is_followed(self, download_patch):
        show = self._get_new_dummy_show()
        show.wait_minutes_for_better_quality = 5

        episode = self._get_new_dummy_episode(show)

        episodedownloadtask = EpisodeDownloadTask()

        episodedownloadtask._get_episodes = MagicMock(return_value=[episode])
        # Don't send actual notifications to users
        episodedownloadtask._notify_user = MagicMock()
        episodedownloadtask._deferred()
        self.assertEqual(download_patch.call_count, 0)

        # It should be downloaded if it was created 10 minutes ago,
        # because it only has to wait for 5 minutes.
        episode.created_at = datetime.now() - timedelta(minutes=10)

        episodedownloadtask._get_episodes = MagicMock(return_value=[episode])
        # Don't send actual notifications to users
        episodedownloadtask._notify_user = MagicMock()
        episodedownloadtask._deferred()
        self.assertEqual(download_patch.call_count, 1)
