import click

from gopro_sync.media import MediaFileManager, filter_media


@click.command()
@click.option("--media", default="image", help="file type to fetch.")
@click.option("--path", default="gopro-media", help="path to save files.")
def gopro_sync_cli(media, path):
    """sync images from go pro."""
    mfm = MediaFileManager()
    mfm.connect()
    images = filter_media(mfm.media, file_extension="JPG")

    for img in images:
        mfm.fetch_file(img)


if __name__ == "__main__":
    gopro_sync_cli()
