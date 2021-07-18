import datetime
import logging
from enum import Enum
from pathlib import Path
from typing import Iterable, List

from .client import GoProClient
from .core import GoProFile, parse_size

logger = logging.getLogger(__name__)


class MediaType(Enum):
    IMAGE = "JPG"
    RAW_IMAGE = "GPR"
    VIDEO = "MP4"
    ALL = "ALL"


class MediaFile:
    def __init__(self, name, size, modified):
        self.name = name
        self.size = parse_size(size)
        self._modified = datetime.datetime.strptime(modified, "%d-%b-%Y %H:%M")

    @classmethod
    def from_gpf(cls, gpf: GoProFile):
        return MediaFile(**gpf)

    def __repr__(self):
        return f"MediaFile({self.name!r})"

    @property
    def extension(self):
        return Path(self.name).suffixes[-1][1:]

    @property
    def modified(self):
        return self._modified.isoformat()

    def fetch(self):
        pass


class MediaFileManager:
    def __init__(self, skip_lowres=True):
        self._skip_lowres = skip_lowres
        self.client = GoProClient()
        self.media: List[MediaFile] = []

    def connect(self):
        raw_files = self.client.get_entries()
        self.media = self._build_media_files(raw_files)

    def export(self, media_type: MediaType, path=None, num=None, dry_run=False):
        path = path or "./gopro-collection"

        if isinstance(path, str):
            path = Path(path)

        path = path.expanduser().absolute()
        path.touch(exist_ok=True)

        target_files = sorted(
            filter_media(self.media, media_type), key=lambda x: x.modified
        )
        candidate_files = target_files[:num]
        total = len(candidate_files)

        if dry_run:
            return candidate_files

        for mf in candidate_files:
            self.fetch_file(mf)

    def _build_media_files(self, gpfiles: List[GoProFile]):
        origin_files = list(
            MediaFile(name=file.name, size=file.size, modified=file.modified)
            for file in gpfiles
        )

        if self._skip_lowres:
            return list(file for file in origin_files if file.extension != "LRV")
        return origin_files

    def fetch_file(self, mf: MediaFile, **kwargs):
        buffer = self.client.fetch_file(mf.name, **kwargs)


def filter_media(media_files: Iterable[MediaFile], media_type: MediaType):
    if media_type == MediaType.ALL:
        return iter(media_files)

    return (file for file in media_files if file.name.endswith(media_type.value))
