from logic import PyLastHelper
import json

user = "gkeep"

ph = PyLastHelper(user)

tracks = ph.get_last_played(10)
print(json.dumps(tracks, indent=2))
