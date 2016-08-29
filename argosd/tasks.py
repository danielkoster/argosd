import logging
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

import feedparser
from peewee import DoesNotExist, IntegrityError

from argosd import settings
from argosd.threading import Threaded
from argosd.models import Show, Episode


class BaseTask(Threaded):
    """Abstract task, provides basic task functionality"""

    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3

    priority = PRIORITY_NORMAL

    def __lt__(self, other):
        """Compare to another task, sort by priority"""
        return self.priority - other.priority

    def deferred(self):
        """A task is run in it's own thread, every exception is logged"""
        try:
            self._deferred()
        except Exception as e:
            logging.critical('Exception in %s: %s', self.get_name(), e)

        logging.info('%s stopped', self.get_name())

    @abstractmethod
    def _deferred(self):
        """The main method of a task"""
        pass


class RSSFeedParserTask(BaseTask):
    """Task to retrieve and download torrents from the RSS feed"""

    def _deferred(self):
        episodes = self._parse_episodes_from_feed()

        # Save all episodes we haven't stored yet
        for episode in episodes:
            logging.debug('Found episode: %s', episode)
            if self._get_existing_episode_from_database(episode) is None:
                try:
                    episode.save()
                except IntegrityError:
                    logging.error('Could not save episode to database')

    def _get_existing_episode_from_database(self, episode):
        """Retrieves an existing episode from the database.
        An episode is equal if it has the same show, season, episode
        and quality. We store multiple show+season+episode Episodes if
        the quality is different so later on we can decide which
        we want to download and perhaps wait for a better quality episode.
        """
        try:
            return Episode.select() \
                .where(Episode.show == episode.show) \
                .where(Episode.season == episode.season) \
                .where(Episode.episode == episode.episode) \
                .where(Episode.quality == episode.quality) \
                .get()
        except DoesNotExist:
            return None

    def _parse_episodes_from_feed(self):
        feed = feedparser.parse(settings.RSS_FEED)

        if not feed.entries:
            logging.error('No episodes found in RSS feed, please check URL')

        shows = Show.select()
        episodes = []
        for item in feed.entries:
            for show in shows:
                if show.title in item.title:
                    episode = self._get_episode_data_from_item(item, show)
                    episodes.append(episode)

                    # Matching show has been found, move on to the next item
                    break

        return episodes

    def _get_episode_data_from_item(self, item, show):
        episode = Episode()
        episode.title = show.title
        episode.link = item.link
        episode.show = show

        # Search for season and episode number
        season_episode_regexes = [
            '[S|s]([0-9]{1,2})[E|e]([0-9]{1,2})',
            '([0-9]{1,2})[X|x]([0-9]{1,2})',
        ]

        for regex in season_episode_regexes:
            matches = re.search(regex, item.title)
            if matches is not None:
                episode.season = int(matches.group(1))
                episode.episode = int(matches.group(2))

                # We've found our season and episode, stop searching
                break

        # Search for quality of the video
        matches = re.search('([0-9]{1,4})[P|p|i]', item.title)
        if matches is not None:
            episode.quality = int(matches.group(1))

        return episode


class EpisodeDownloadTask(BaseTask):

    def _deferred(self):
        episodes = self._get_episodes()
        now = datetime.now()

        for episode in episodes:
            download_after = episode.created_at + timedelta(
                minutes=episode.show.wait_minutes_for_better_quality)

            if now > download_after or \
                    episode.quality >= settings.QUALITY_THRESHOLD:

                self._download_episode(episode)

                # Delete all episodes from this show+season+episode
                # so we don't download another quality variant.
                to_delete = [item for item in episodes if
                             item != episode and
                             item.show == episode.show and
                             item.season == episode.season and
                             item.episode == episode.episode]

                for episode in to_delete:
                    episode.delete_instance()

                to_delete.append(episode)

                # Remove all of them from the list so we don't iterate
                # over them again. Alter the original list we are using.
                episodes[:] = [episode for episode in episodes if
                               episode not in to_delete]

    def _get_episodes(self):
        """Get all non-downloaded episodes, order with highest quality first"""
        # TODO: Remove hack to pass PEP8 by checking is_downloaded bool == 0
        return list(Episode.select()
                    .where(Episode.is_downloaded == 0)
                    .order_by(Episode.quality.desc()))

    def _download_episode(self, episode):
        """Add the torrent from the episode to a download application"""

        # TODO: Add torrent to download application

        episode.is_downloaded = True
        episode.save()
