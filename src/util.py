import os
from pathlib import Path

import appdirs


# class DataManager:
#     def __init__(self):
#         self.base_folder = (DirManager().cache_dir())
#
#         if not os.path.exists(self.base_folder / "images"):
#             if not os.path.exists(self.base_folder):
#                 os.mkdir(self.base_folder)
#             os.mkdir(self.base_folder / "images")
#
#     def cleanup(self):
#         try:
#             shutil.rmtree(self.base_folder)
#         except FileNotFoundError:
#             logging.error("Couldn't remove temp folder")
#         finally:
#             logging.debug("Successfully removed temp folder")
#
#         if not os.path.exists(self.base_folder / "images"):
#             if not os.path.exists(self.base_folder):
#                 os.mkdir(self.base_folder)
#             os.mkdir(self.base_folder / "images")
#
#     def cache_images(self, metadata):
#         logging.debug("caching images...")
#         for image in metadata:
#             filename = self.base_folder / "images" / image["album_id"]
#             link = image["image_link"]
#             try:
#                 if not os.path.exists(filename):
#                     _req = requests.get(link, timeout=2)
#                     with open(filename, "wb") as file:
#                         file.write(_req.content)
#                         logging.debug(f"saved album art with id=[{image['album_id']}]")
#                 else:
#                     logging.debug(f"album art [{image['album_id']}] is already cached")
#             except requests.exceptions.ConnectionError as error:
#                 logging.error("Couldn't download {}: {}".format(link, error))
#             except requests.exceptions.MissingSchema as error:
#                 logging.debug("Broken image link: {}".format(error))


class DirManager:
    def __init__(self):
        author = "gkeep"
        app_name = "lastfm-stats"

        self.config_directory = appdirs.user_config_dir(app_name, author)
        self.cache_directory = appdirs.user_cache_dir(app_name, author)
        self.log_directory = appdirs.user_log_dir(app_name, author)

        os.makedirs(self.config_directory, exist_ok=True)
        os.makedirs(self.cache_directory, exist_ok=True)
        os.makedirs(self.log_directory, exist_ok=True)

    def config_dir(self) -> Path:
        return Path(self.config_directory)

    def cache_dir(self) -> Path:
        return Path(self.cache_directory)

    def log_dir(self) -> Path:
        return Path(self.log_directory)