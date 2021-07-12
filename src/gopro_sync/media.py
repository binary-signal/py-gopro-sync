import datetime
from collections import namedtuple
from copy import copy
from pathlib import Path
from typing import NamedTuple

from .client import GoProClient
from .core import FileSizeMeta, GoProFile, parse_size  # noqa

MediaFileMeta = namedtuple("MediaFileMeta", "gpf modified size")


class MediaFile(NamedTuple):
    name: str
    meta: MediaFileMeta


MediaFile = namedtuple("MediaFile", "name meta")  # noqa


def filter_media(md_files: list[MediaFile], file_extension: str = ".*"):
    if file_extension == ".*":
        return md_files

    for file in md_files:
        if file.name.endswith(file_extension):
            yield file


class MediaFile:
    def __init__(self, gpf: GoProFile):
        self._gpf = copy(gpf)
        self.name = gpf.name
        self.size = parse_size(gpf.size)
        self.modified = datetime.datetime.strptime(gpf.modified, "%d-%b-%Y %H:%M")

    def fetch(self):
        pass


class JpgImage(MediaFile):
    pass


class RawImage(MediaFile):
    pass


class Mp4Video(MediaFile):
    pass


class MediaFileManager:
    def __init__(self, sync_dir):
        self.client = GoProClient()

        self.media: list[MediaFile] = []
        self.sync_dir = Path(sync_dir).expanduser().absolute()

    def connect(self):
        raw_files = self.client.get_entries()
        self.media = self._build_media_files(raw_files)

    def _build_media_files(self, gpfiles: list[GoProFile]):
        return list(
            MediaFile(
                name=file.name,
                meta=MediaFileMeta(
                    {
                        "gpf": file,
                        "size": parse_size(file.size),
                        "modified": datetime.datetime.strptime(
                            file.modified, "%d-%b-%Y %H:%M"
                        ),
                    }
                ),
            )
            for file in gpfiles
        )

    def fetch_file(self, md: MediaFile):
        self.client.fetch_file(md.meta["gpf"])
