import logging
from io import BytesIO
from itertools import islice

from bs4 import BeautifulSoup
from requests import Session

from .core import GoProFile

logger = logging.getLogger(__name__)


class GoProSyncException(Exception):
    pass


class GoProNotFound(GoProSyncException):
    pass


class GoProClient:
    url = "http://10.5.5.9/videos/DCIM/100GOPRO/"

    def __init__(self):
        self.http_session = Session()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def get_entries(self):
        """Return `GoProFile` objects, raw objects parsed from html rows"""
        response = self.http_session.get(self.url)

        # from gopro_sync.mocks.html_raw import go_pro_html_reponse  # noqa

        soup = BeautifulSoup(response.text, "lxml")

        trs = soup.find_all("tr", recursive=True)
        magic_offset = 3

        raw_entries = islice(trs, magic_offset, None)

        _get_name = lambda x: x.contents[0].attrs["href"]
        _get_modified = lambda x: x.contents[0].strip()
        _get_size = lambda x: x.contents[0].strip()

        def _parse_gpf(entry):
            _name, _modified, _size = entry
            name = _get_name(_name)
            modified = _get_modified(_modified)
            size = _get_size(_size)

            return GoProFile(name, modified, size)

        return list(map(_parse_gpf, raw_entries))

    def fetch_file(self, file_name: str, **kwargs):
        logger.info(f"fetching {file_name = }")

        url = self.url + file_name.split("/")[-1]
        local_filename = url.split("/")[-1]

        with self.http_session.get(url, stream=True) as r:
            r.raise_for_status()
            buffer = BytesIO()
            for chunk in r.iter_content(chunk_size=2048):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                buffer.write(chunk)
        return buffer
