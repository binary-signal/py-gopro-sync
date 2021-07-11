from collections import namedtuple

from .client import GoProClient
from .core import FileSizeMeta, GoProFile

MediaFile = namedtuple("MediaFile", "name meta")


def filter_media(md_files: list[MediaFile], file_extension: str = ".*"):
    if file_extension == ".*":
        return md_files

    for file in md_files:
        if file.name.endswith(file_extension):
            yield file


class MediaFileManager:
    def __init__(self):
        # self._gpv = list(gpv)
        self.client = GoProClient()
        self.media: list = []

    def connect(self):
        raw_files = self.client.get_entries()
        self.media = self._build_media_table(raw_files)

    def _build_media_table(self, gpfiles: list[GoProFile]):
        return list(
            MediaFile(
                name=file.name,
                meta={"gpf": file, "size": self._parse_size(file.size)},
            )
            for file in gpfiles
        )

    def fetch_file(self, md: MediaFile):
        self.client.fetch_file(md.meta["gpf"])

    @classmethod
    def _parse_size(cls, size_str) -> FileSizeMeta:
        value, unit = float(size_str[:-1]), size_str[-1]

        GB = 1024 * 1024 * 1024
        MB = 1024 * 1024
        KB = 1024

        unit_mapping = {"G": GB, "M": MB, "k": KB}

        size_in_bytes = value * unit_mapping[unit]

        def human_readable_size(self):
            return f"{self.value!r} {self.unit}"

        FileSizeMeta.human_readable_size = human_readable_size

        return FileSizeMeta(value, unit, size_in_bytes)
