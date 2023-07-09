import os
import pylast

# NOTE: probably should remove this and add proper authentication instead of using my api keys
API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
)


def get_last_played(user: str, limit: int = 10) -> list:
    """
    Get last played songs from user
    :param user: a last.fm user
    :param limit: number of songs to get
    :return: list of songs (artist, track, album, cover url)
    """
    tracks = []
    raw = lastfm_network.get_user(user).get_recent_tracks(limit)

    for i in range(0, len(raw)):
        track_data = raw[i].track
        album = "ERR"
        if track_data.get_album():
            album = track_data.get_album().get_name()

        track = {
            "artist": track_data.artist.name,
            "track":  track_data.title,
            "album":  album
        }

        track.update({
            "cover_url": pylast.Album(track["artist"], track["album"], lastfm_network).get_cover_image(size=2)
        })
        tracks.append(track)

    return tracks


def get_top_played(user: str, limit: int = 10, period: str = 'PERIOD_1MONTH') -> list:
    """
    Get top songs
    :param user: a last.fm user
    :param limit: number of songs to get
    :param period: time period: ``PERIOD_7DAYS``, ``PERIOD_1MONTH``, ``PERIOD_3MONTHS``,
                                ``PERIOD_6MONTHS``, ``PERIOD_12MONTHS``, ``PERIOD_OVERALL``
    :return: list of songs (artist, track)
    """
    # INFO:
    #   1. for some reason period argument doesn't work in get_top_tracks()
    #   2. not all tracks have an album assossiated with them, so we can't reliably get a cover image
    tracks = []
    raw = lastfm_network.get_user(user).get_top_tracks(period=period, limit=limit)

    for i in range(0, len(raw)):
        track_data = raw[i].item

        track = {
            "artist": track_data.artist.name,
            "track":  track_data.title,
        }

        tracks.append(track)

    return tracks
