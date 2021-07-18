import logging
from collections import Counter
from pathlib import Path

import click
from rich.console import Console

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
    "--sync-path",
    default=Path("./gopro-media"),
    type=click.Path(writable=True),
    show_default=True,
    help="Export files to local  path",
)
@click.option(
    "--skip-lowres", default=True, show_default=True, help="Skip low resolution files"
)
def gopro_sync_cli(media_type, sync_path, skip_lowres):
    """Sync gopro media file via wifi.

    Select `media_type` to sync
    """

    console = Console()

    media_type = MediaType[sanitize(media_type)]
    sync_path = Path(sync_path)

    logger.info(f"{media_type = }, {sync_path = }, {skip_lowres = }")

    mfm = MediaFileManager(skip_lowres=skip_lowres)

    mfm.connect()
    logger.info(Counter(map(lambda x: x.extension, mfm.media)))

    candidate_files = mfm.export(media_type, dry_run=True)

    file_count = len(candidate_files)
    logger.info(f"found {file_count} candidate file | {media_type.name}")

    if not candidate_files:
        console.print("Nothing to sync.")
        raise SystemExit(0)

    if not sync_path.exists():
        sync_path.mkdir(parents=True)

    # get size in bytes of bytesIO buffer
    file_size = lambda x: x.getbuffer().nbytes
    bytes_synced = 0
    MB = 1024 * 1014
    count = 1
    for file in candidate_files:
        file_obj = mfm.client.fetch_file(file.name)
        file_path = sync_path.joinpath(Path(file.name).parts[-1])
        with open(file_path, "wb") as file_handle:
            file_handle.write(file_obj.getbuffer())
            bytes_synced += file_size(file_obj)
        count += 1

    console.print(f"Synced {count} {media_type.name} files")
    console.print(f"Transfered {bytes_synced / MB:.2f} mb")
    console.print(f"Sync folder: {sync_path.absolute()}")


if __name__ == "__main__":
    gopro_sync_cli()
