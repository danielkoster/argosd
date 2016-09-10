from peewee import *

from argosd import settings


class BaseModel(Model):
    """Abstract model. Sets the database."""

    class Meta:
        database = SqliteDatabase('{}/argosd.db'.format(settings.ARGOSD_PATH))


class Show(BaseModel):
    """TV show we need to download from RSS feeds."""

    id = PrimaryKeyField()
    title = CharField(unique=True)
    follow_from_season = IntegerField()
    follow_from_episode = IntegerField()
    # Minimum quality an episode should be
    quality_threshold = IntegerField()
    tmdb_id = IntegerField(null=True)
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

    class Meta:
        indexes = (
            # Unique key on show/season/episode/quality
            (('show', 'season', 'episode', 'quality'), True),
        )
