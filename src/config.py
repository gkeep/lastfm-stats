from pathlib import Path
from time import time

from util import DirManager


class CfgManager:
    def __init__(self):
        dirs = DirManager()

        self.log_path = f"{dirs.log_dir()}/{round(time())}"

    def get_log(self):
        return Path(self.log_path)
