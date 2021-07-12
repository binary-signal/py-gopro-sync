import logging
from collections import Counter

import click

from gopro_sync.media import MediaFileManager, MediaType

logger = logging.getLogger(__name__)

desanitize = lambda x: x.name.lower().replace("_", "-")
sanitize = lambda x: x.upper().replace("-", "_")

_choices = list(map(desanitize, list(MediaType)))


@click.command()
@click.option(
    "-m",
    "--media-type",
    required=True,
    type=click.Choice(_choices, case_sensitive=False),
    help="Media type to sync",
)
@click.option(
    "--path", type=click.Path(writable=True), help="Export files to local  path"
)
@click.option(
    "--skip-lowres", default=True, show_default=True, help="Skip low resolution files"
)
def gopro_sync_cli(media_type, path, skip_lowres):
    """Sync gopro media file via wifi."""

    media_type = sanitize(media_type)

    logger.info(media_type)
    mfm = MediaFileManager(skip_lowres=skip_lowres)
    mfm.connect()

    logger.info(Counter(map(lambda x: x.extension, mfm.media)))
    candidate_files = mfm.export(MediaType[media_type], dry_run=True)
    file_count = len(candidate_files)
    logger.info(f"found {file_count} candidate file")
    count = 1
    for file in candidate_files:
        mfm.client.fetch_file(file.name)
        count += 1


if __name__ == "__main__":
    gopro_sync_cli()
