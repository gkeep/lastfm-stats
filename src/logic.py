import os
import pylast

API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
)


def get_last_played_tracks(user: str, amount: int = 10) -> list:
    tracks = []
    raw = lastfm_network.get_user(user).get_recent_tracks(amount)

    for i in range(0, len(raw)):
        track_data = raw[i].track
        track = {
            "artist": track_data.artist.name,
            "track":  track_data.title,
            "album":  raw[i].album,
        }

        track.update({
                "cover_url": pylast.Album(track["artist"], track["album"], lastfm_network).get_cover_image(size=2)
            })
        tracks.append(track)

    return tracks
