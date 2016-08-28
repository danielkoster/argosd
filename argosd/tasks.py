import logging
import re
from abc import ABCMeta, abstractmethod

import feedparser

from argosd import settings
from argosd.threading import Threaded


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
        logging.debug('Matching shows found: %d', len(episodes))

    def _parse_episodes_from_feed(self):
        feed = feedparser.parse(settings.RSS_FEED)

        if not feed.entries:
            logging.error('No episodes found in RSS feed, please check URL')

        shows = self.get_all_shows()
        episodes = []
        for item in feed.entries:
            for show in shows:
                if show['title'] in item.title:
                    episode = self._get_episode_data_from_item(item, show)
                    episodes.append(episode)

                    # Matching show has been found, move on to the next item
                    break

        return episodes

    def get_all_shows(self):
        """Returns a list of all the shows we want to follow"""
        # TODO: replace this with persistent Show objects
        return [
            {
                'id': 1,
                'title': 'SciTech Now',
            },
        ]

    def _get_episode_data_from_item(self, item, show):
        episode = {
            'title': show['title'],
            'link': item.link,
            'show_id': show['id'],
        }

        # Search for season and episode number
        season_episode_regexes = [
            '[S|s]([0-9]{1,2})[E|e]([0-9]{1,2})',
            '([0-9]{1,2})[X|x]([0-9]{1,2})',
        ]

        for regex in season_episode_regexes:
            matches = re.search(regex, item.title)
            if matches is not None:
                episode['season'] = int(matches.group(1))
                episode['episode'] = int(matches.group(2))

                # We've found our season and episode, stop searching
                break

        # Search for quality of the video
        matches = re.search('([0-9]{1,4})[P|p|i]', item.title)
        if matches is not None:
            episode['quality'] = int(matches.group(1))

        return episode
