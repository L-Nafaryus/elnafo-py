from peewee import *

database = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): 
        pass

class BaseModel(Model):
    class Meta:
        database = database

class AlbumAttributes(BaseModel):
    entity_id = IntegerField(index = True, null = True)
    key = TextField(null = True)
    value = TextField(null = True)

    class Meta:
        table_name = 'album_attributes'
        indexes = (
            (('entity_id', 'key'), True),
        )

class Albums(BaseModel):
    added = FloatField(null = True)
    album = TextField(null = True)
    albumartist = TextField(null = True)
    albumartist_credit = TextField(null = True)
    albumartist_sort = TextField(null = True)
    albumdisambig = TextField(null = True)
    albumstatus = TextField(null = True)
    albumtype = TextField(null = True)
    artpath = BlobField(null = True)
    asin = TextField(null = True)
    catalognum = TextField(null = True)
    comp = IntegerField(null = True)
    country = TextField(null = True)
    day = IntegerField(null = True)
    disctotal = IntegerField(null = True)
    genre = TextField(null = True)
    label = TextField(null = True)
    language = TextField(null = True)
    mb_albumartistid = TextField(null = True)
    mb_albumid = TextField(null = True)
    mb_releasegroupid = TextField(null = True)
    month = IntegerField(null = True)
    original_day = IntegerField(null = True)
    original_month = IntegerField(null = True)
    original_year = IntegerField(null = True)
    r128_album_gain = IntegerField(null = True)
    releasegroupdisambig = TextField(null = True)
    rg_album_gain = FloatField(null = True)
    rg_album_peak = FloatField(null = True)
    script = TextField(null = True)
    year = IntegerField(null = True)

    class Meta:
        table_name = 'albums'

class ItemAttributes(BaseModel):
    entity_id = IntegerField(index = True, null = True)
    key = TextField(null = True)
    value = TextField(null = True)

    class Meta:
        table_name = 'item_attributes'
        indexes = (
            (('entity_id', 'key'), True),
        )

class Items(BaseModel):
    acoustid_fingerprint = TextField(null = True)
    acoustid_id = TextField(null = True)
    added = FloatField(null = True)
    album = TextField(null = True)
    album_id = IntegerField(null = True)
    albumartist = TextField(null = True)
    albumartist_credit = TextField(null = True)
    albumartist_sort = TextField(null = True)
    albumdisambig = TextField(null = True)
    albumstatus = TextField(null = True)
    albumtype = TextField(null = True)
    arranger = TextField(null = True)
    artist = TextField(null = True)
    artist_credit = TextField(null = True)
    artist_sort = TextField(null = True)
    asin = TextField(null = True)
    bitdepth = IntegerField(null = True)
    bitrate = IntegerField(null = True)
    bpm = IntegerField(null = True)
    catalognum = TextField(null = True)
    channels = IntegerField(null = True)
    comments = TextField(null = True)
    comp = IntegerField(null = True)
    composer = TextField(null = True)
    composer_sort = TextField(null = True)
    country = TextField(null = True)
    day = IntegerField(null = True)
    disc = IntegerField(null = True)
    disctitle = TextField(null = True)
    disctotal = IntegerField(null = True)
    encoder = TextField(null = True)
    format = TextField(null = True)
    genre = TextField(null = True)
    grouping = TextField(null = True)
    initial_key = TextField(null = True)
    label = TextField(null = True)
    language = TextField(null = True)
    length = FloatField(null = True)
    lyricist = TextField(null = True)
    lyrics = TextField(null = True)
    mb_albumartistid = TextField(null = True)
    mb_albumid = TextField(null = True)
    mb_artistid = TextField(null = True)
    mb_releasegroupid = TextField(null = True)
    mb_releasetrackid = TextField(null = True)
    mb_trackid = TextField(null = True)
    media = TextField(null = True)
    month = IntegerField(null = True)
    mtime = FloatField(null = True)
    original_day = IntegerField(null = True)
    original_month = IntegerField(null = True)
    original_year = IntegerField(null = True)
    path = BlobField(null = True)
    r128_album_gain = IntegerField(null = True)
    r128_track_gain = IntegerField(null = True)
    releasegroupdisambig = TextField(null = True)
    rg_album_gain = FloatField(null = True)
    rg_album_peak = FloatField(null = True)
    rg_track_gain = FloatField(null = True)
    rg_track_peak = FloatField(null = True)
    samplerate = IntegerField(null = True)
    script = TextField(null = True)
    title = TextField(null = True)
    track = IntegerField(null = True)
    tracktotal = IntegerField(null = True)
    year = IntegerField(null = True)

    class Meta:
        table_name = 'items'

