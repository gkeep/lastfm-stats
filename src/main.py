from logic import PyLastHelper
import json
import logging
from config import CfgManager

logger = logging.getLogger(__name__)
logging.basicConfig(filename=CfgManager().get_log(), filemode='w', level=logging.DEBUG)
logging.getLogger('pylast').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)


def main():
    user = "gkeep"
    ph = PyLastHelper(user)
    tracks = ph.get_top_played(10, "PERIOD_1MONTH")
    print(json.dumps(tracks, indent=2))


main()
