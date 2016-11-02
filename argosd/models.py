import logging

from peewee import *
from playhouse.shortcuts import model_to_dict

from argosd import settings
from argosd.torrentclient import Transmission, TorrentClientException, \
    TorrentAlreadyDownloadedException


class BaseModel(Model):
    """Abstract model. Sets the database."""

    def to_dict(self):
        """Represents this object as a dictionary."""
        return model_to_dict(self)

    class Meta:
        database = SqliteDatabase('{}/argosd.db'.format(settings.ARGOSD_PATH))


class Show(BaseModel):
    """TV show we need to download from RSS feeds."""

    id = PrimaryKeyField()
    title = CharField(unique=True)
    follow_from_season = IntegerField()
    follow_from_episode = IntegerField()
    minimum_quality = IntegerField()
    wait_minutes_for_better_quality = IntegerField(default=0)


class Episode(BaseModel):
    """Episodes related to TV shows."""

    id = PrimaryKeyField()
    show = ForeignKeyField(Show, related_name='episodes')
    link = CharField()
    season = IntegerField()
    episode = IntegerField()
    quality = IntegerField()
    is_downloaded = BooleanField(default=False)
    created_at = TimestampField()

    def __unicode__(self):
        return '{} - S{} - E{} - Q{}'.format(
            self.show.title, self.season, self.episode, self.quality)

    def to_dict(self):
        """Represents this object as a dictionary.

        created_at is converted seperately because a datetime object
        is not JSON serializable."""
        representation = model_to_dict(self, exclude=[
            Episode.created_at, Episode.link])
        representation['created_at'] = int(self.created_at.strftime('%s'))
        return representation

    def download(self):
        """Add the torrent from the episode to a torrent client.

        Returns True if the episode is downloaded, or False if
        something went wrong."""
        try:
            torrentclient = Transmission()
            torrentclient.download_episode(self)

            self.is_downloaded = True
            self.save()

            logging.info('Downloaded episode: %s', self)
            return True
        except TorrentAlreadyDownloadedException:
            logging.info('Already downloaded episode %s, '
                         'marking as downloaded', self)
            self.is_downloaded = True
            self.save()
            return True
        except TorrentClientException as e:
            logging.critical('TorrentClientException: %s', e)
            return False

    class Meta:
        indexes = (
            # Unique key on show/season/episode/quality
            (('show', 'season', 'episode', 'quality'), True),
        )
