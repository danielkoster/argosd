import logging
import re
from abc import abstractmethod
from datetime import datetime, timedelta

import feedparser
from peewee import DoesNotExist, IntegrityError

from argosd import settings
from argosd.bots import TelegramBot
from argosd.threading import Threaded
from argosd.models import Show, Episode
from argosd.torrentclient import Transmission, CorruptTorrentException


class BaseTask(Threaded):
    """Abstract task, provides basic task functionality."""

    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3

    priority = PRIORITY_NORMAL

    def __lt__(self, other):
        """Compare to another task, sort by priority."""
        return self.priority - other.priority

    def deferred(self):
        """A task is run in it's own thread, every exception is logged."""
        try:
            self._deferred()
        except Exception as e:
            logging.critical('Exception in %s: %s', self.get_name(), e)

        logging.debug('%s stopped', self.get_name())

    @abstractmethod
    def _deferred(self):
        """The main method of a task."""
        raise NotImplementedError


class RSSFeedParserTask(BaseTask):
    """Task to retrieve and download torrents from the RSS feed."""

    def _deferred(self):
        episodes = self._parse_episodes_from_feed()

        logging.debug('Relevant episodes found in RSS feed: %d', len(episodes))

        # Save all episodes we haven't stored yet
        for episode in episodes:
            logging.debug('Found episode: %s', episode)
            if self._get_existing_episode_from_database(episode) is None:
                try:
                    episode.save()
                    self._notify_user(episode)
                    logging.info('Saved episode: %s', episode)
                except IntegrityError:
                    logging.error('Could not save episode to database')

    @staticmethod
    def _get_existing_episode_from_database(episode):
        """Retrieves an existing episode from the database.
        An episode is equal if it has the same show, season, episode
        and quality. We store multiple show+season+episode Episodes if
        the quality is different so later on we can decide which
        we want to download and perhaps wait for a better quality episode."""
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

        episodes = []
        for feed_item in feed.entries:
            show = self._get_matching_show(feed_item)
            if show:
                episode = self._get_episode_data_from_item(feed_item, show)

                quality_check = episode.quality is not None and \
                    episode.quality >= show.minimum_quality

                follow_check = episode.season > show.follow_from_season or \
                    (episode.season == show.follow_from_season and
                        episode.episode >= show.follow_from_episode)

                is_downloaded = self._is_episode_downloaded(episode)

                if quality_check and follow_check and not is_downloaded:
                    episodes.append(episode)

        return episodes

    @staticmethod
    def _is_episode_downloaded(episode):
        """Checks if this item has already been downloaded."""
        try:
            Episode.select() \
                .where(Episode.show == episode.show) \
                .where(Episode.season == episode.season) \
                .where(Episode.episode == episode.episode) \
                .where(Episode.is_downloaded == 1) \
                .get()
            return True
        except DoesNotExist:
            return False

    def _get_matching_show(self, feed_item):
        shows = Show.select()
        for show in shows:
            if self._match_titles(show.title, feed_item.title):
                return show

    @staticmethod
    def _match_titles(title_show, title_feed_item):
        # Strip all except letters, numbers and spaces and convert to lowercase
        title_show = re.sub('[^a-zA-Z0-9 ]', '', title_show).lower()
        title_feed_item = re.sub('[^a-zA-Z0-9 ]', '', title_feed_item).lower()
        return title_show in title_feed_item

    @staticmethod
    def _get_episode_data_from_item(item, show):
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

    @staticmethod
    def _notify_user(episode):
        """Sends the user a notification about this episode."""
        if settings.TELEGRAM_BOT_TOKEN:
            bot = TelegramBot()
            text = 'A new episode has been found!\n' \
                   '{} - S{}E{} - {}p'
            text = text.format(episode.show.title, episode.season,
                               episode.episode, episode.quality)

            callback_data = 'download {}'.format(episode.id)
            reply_markup = bot.create_button_markup('Download now',
                                                    callback_data)

            bot.send_message(text, reply_markup=reply_markup)


class EpisodeDownloadTask(BaseTask):
    """Task to retrieve episodes ready to be downloaded and sending them
    to a torrentclient."""

    def _deferred(self):
        episodes = self._get_episodes()
        torrentclient = Transmission()

        for episode in episodes:
            download_after = episode.created_at + timedelta(
                minutes=episode.show.wait_minutes_for_better_quality)

            if datetime.now() > download_after or \
                    episode.quality >= settings.QUALITY_THRESHOLD:

                try:
                    torrentclient.download_episode(episode)
                    episode.is_downloaded = True
                    episode.save()

                    # Send the user a notification about this episode
                    self._notify_user(episode)

                    # Delete all episodes from this show+season+episode
                    # so we don't download another quality variant.
                    to_delete = [item for item in episodes if
                                 item != episode and
                                 item.show == episode.show and
                                 item.season == episode.season and
                                 item.episode == episode.episode]
                except CorruptTorrentException:
                    # The torrent for to this episode is corrupt, delete it
                    to_delete = [episode]

                for episode in to_delete:
                    episode.delete_instance()

                to_delete.append(episode)

                # Remove all of them from the list so we don't iterate
                # over them again. Alter the original list we are using.
                episodes[:] = [episode for episode in episodes if
                               episode not in to_delete]

    @staticmethod
    def _get_episodes():
        """Get all non-downloaded episodes, order by highest quality first."""
        return list(Episode.select()
                    .where(Episode.is_downloaded == 0)
                    .order_by(Episode.quality.desc()))

    @staticmethod
    def _notify_user(episode):
        """Sends the user a notification about this episode."""
        if settings.TELEGRAM_BOT_TOKEN:
            bot = TelegramBot()
            text = 'A new episode has been downloaded!\n' \
                   '{} - S{}E{} - {}p'
            text = text.format(episode.show.title, episode.season,
                               episode.episode, episode.quality)
            bot.send_message(text)
