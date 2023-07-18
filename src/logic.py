import os
import pylast


# NOTE: probably should remove this and add proper authentication instead of using my api keys
API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]


class PyLastHelper:
    def __init__(self, user):
        self.lastfm_network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        self.userdata = self.lastfm_network.get_user(user)

    def get_last_played(self, limit: int = 10) -> list:
        """
        Get last played songs from user
        :param limit: number of songs to get
        :return: list of songs (artist, track, album, cover url)
        """
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
                pass
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
        #   2. not all tracks have an album assossiated with them, so we can't reliably get a cover image
        tracks = []
        raw = self.userdata.get_top_tracks(period=period, limit=limit)

        for i in range(0, len(raw)):
            track_data = raw[i].item

            track = {
                "artist": track_data.artist.name,
                "track": track_data.title,
            }

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

    assert res == [
        {'artist': 'The Dillinger Escape Plan', 'track': '43% Burnt'},
        {'artist': 'The Dillinger Escape Plan', 'track': 'Sugar Coated Sour'},
        {'artist': 'The Dillinger Escape Plan', 'track': 'Jim Fear'},
        {'artist': 'The Dillinger Escape Plan', 'track': 'X#..'},
        {'artist': 'The Dillinger Escape Plan', 'track': "Destro's Secret"}
    ]


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
