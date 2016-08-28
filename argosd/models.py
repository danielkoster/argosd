from peewee import *

from argosd import settings


class BaseModel(Model):

    class Meta:
        database = SqliteDatabase('{}/argosd.db'.format(settings.ARGOSD_PATH))


class Show(BaseModel):

    id = PrimaryKeyField()
    title = CharField(unique=True)
    follow_from_season = IntegerField()
    follow_from_episode = IntegerField()
    quality_threshold = IntegerField()
    tmdb_id = IntegerField(null=True)


class Episode(BaseModel):

    id = PrimaryKeyField()
    show = ForeignKeyField(Show, related_name='episodes')
    link = CharField()
    season = IntegerField()
    episode = IntegerField()
    quality = IntegerField()
    is_downloaded = BooleanField(default=False)
    created_at = TimestampField()
