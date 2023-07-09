import logic
import json

user = "gkeep"

tracks = logic.get_top_played(user, 10)
print(json.dumps(tracks, indent=2))
