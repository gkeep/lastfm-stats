import os
import pylast
import logging

API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]

logger = logging.getLogger(__name__)


class PyLastHelper:
    def __init__(self, user):
        self.lastfm_network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        self.user = user
        self.userdata = self.lastfm_network.get_user(user)

    def get_last_played(self, limit: int = 10) -> list:
        """
        Get last played songs from user
        :param limit: number of songs to get
        :return: list of songs (artist, track, album, cover url)
        """

        logger.debug(f"getting last {limit} tracks for {self.user}")

        tracks = []
        raw = self.userdata.get_recent_tracks(limit)

        for i in range(0, len(raw)):
            track_data = raw[i].track

            track = {
                "artist": track_data.artist.name,
                "track": track_data.title,
            }

            if track_data.get_album():
                track.update({
                    "album": track_data.get_album().get_name(),
                    "cover_url": pylast.Album(track["artist"], track_data.get_album().get_name(),
                                              self.lastfm_network).get_cover_image(size=2)
                })
            else:
                logger.warning(f"Album unknown for {track}, no album name and cover art available (upstream API issue)")

            logger.debug(f"got {track}")
            tracks.append(track)

        return tracks

    def get_top_played(self, limit: int = 10, period: str = 'PERIOD_1MONTH') -> list:
        """
        Get top songs
        :param limit: number of songs to get
        :param period: time period: ``PERIOD_7DAYS``, ``PERIOD_1MONTH``, ``PERIOD_3MONTHS``,
                                    ``PERIOD_6MONTHS``, ``PERIOD_12MONTHS``, ``PERIOD_OVERALL``
        :return: list of songs (artist, track)
        """
        # INFO:
        #   1. for some reason period argument doesn't work in get_top_tracks()
        #   2. not all tracks have an album associated with them, so we can't reliably get a cover image

        logger.debug(f"getting top {limit} tracks for {self.user}, period - {period}")

        tracks = []
        raw = self.userdata.get_top_tracks(period=period, limit=limit)

        for i in range(0, len(raw)):
            track_data = raw[i].item

            track = {
                "artist": track_data.artist.name,
                "track": track_data.title,
            }

            if track_data.get_album():
                track.update({
                    "album": track_data.get_album().get_name(),
                    "cover_url": pylast.Album(track["artist"], track_data.get_album().get_name(),
                                              self.lastfm_network).get_cover_image(size=2)
                })
            else:
                logger.warning(f"Album unknown for {track}, no album name and cover art available (upstream API issue)")

            logger.debug(f"got {track}")
            tracks.append(track)

        return tracks

    def get_top_artists(self, limit: int = 10) -> list:
        data = []
        userdata = self.userdata.get_top_artists(limit=limit)
        raw = userdata

        for i in range(0, len(raw)):
            data.append({"artist": raw[i].item.name})

        return data


def test_get_top_played():
    ph = PyLastHelper("test")
    res = ph.get_top_played(limit=5)

    assert res == [{'album': 'Calculating Infinity',
                    'artist': 'The Dillinger Escape Plan',
                    'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/56360fd323eb4bbb8a8db1864cbab41d.jpg',
                    'track': '43% Burnt'},
                   {'album': 'Calculating Infinity',
                    'artist': 'The Dillinger Escape Plan',
                    'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/56360fd323eb4bbb8a8db1864cbab41d.jpg',
                    'track': 'Sugar Coated Sour'},
                   {'album': 'Calculating Infinity',
                    'artist': 'The Dillinger Escape Plan',
                    'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/56360fd323eb4bbb8a8db1864cbab41d.jpg',
                    'track': 'Jim Fear'},
                   {'artist': 'The Dillinger Escape Plan', 'track': 'X#..'},
                   {'album': "Cursed, Unshaven and Misbehavin': Live Infinity",
                    'artist': 'The Dillinger Escape Plan',
                    'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/75df1b826f8cb0debf09d476d8c8bdd8.jpg',
                    'track': "Destro's Secret"}]


def test_get_last_played():
    ph = PyLastHelper("test")
    res = ph.get_last_played(limit=5)

    assert res == [
        {'artist': 'Nine Inch Nails', 'track': 'The Line Begins to Blur', 'album': 'With Teeth',
         'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/f4241803c93d47478518a5b33e71f0ab.png'},
        {'artist': 'Nine Inch Nails', 'track': 'The Hand That Feeds', 'album': 'With Teeth',
         'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/f4241803c93d47478518a5b33e71f0ab.png'},
        {'artist': 'Nine Inch Nails', 'track': 'The Collector', 'album': 'With Teeth',
         'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/f4241803c93d47478518a5b33e71f0ab.png'},
        {'artist': 'Nine Inch Nails', 'track': 'All the Love in the World', 'album': 'With Teeth',
         'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/f4241803c93d47478518a5b33e71f0ab.png'},
        {'artist': 'Architecture in Helsinki', 'track': "What's In Store?", 'album': 'In Case We Die',
         'cover_url': 'https://lastfm.freetls.fastly.net/i/u/174s/6192ad04cb9c4a2ebc4a02b591b30c70.png'}]


def test_get_top_artists():
    ph = PyLastHelper("test")
    res = ph.get_top_artists(limit=10)

    assert res == [{'artist': 'The Dillinger Escape Plan'}, {'artist': 'David Bowie'}, {'artist': 'Ferry Corsten'},
                   {'artist': 'Sparta'}, {'artist': 'Frank Zappa'}, {'artist': 'The Icarus Line'},
                   {'artist': 'mclusky'}, {'artist': 'Air'}, {'artist': 'Atreyu'}, {'artist': 'Mission of Burma'}]
