import logic
import json

user = "gkeep"

tracks = logic.get_last_played_tracks(user)
print(json.dumps(tracks, indent=2))
