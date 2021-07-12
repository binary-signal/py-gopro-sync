import click

from gopro_sync.media import MediaFileManager, filter_media


@click.command()
@click.option(
    "--media",
    default="image",
    type=click.Choice(["image"], case_sensitive=False),
    help="file type to fetch.",
)
@click.option("--path", default="gopro-media", help="path to save files.")
def gopro_sync_cli(media, path):
    """sync images from go pro."""
    mfm = MediaFileManager(sync_dir=path)
    image_choices = "jpg raw all".split()

    # jpg
    # raw
    # all

    # video

    # clean
    # remove LVR ?
    mfm.connect()
    #
    # if media.lower() == "image":
    #     file_extension = "jpg"
    # elif media.lower() == "video":
    #     file_extension = "mp4"
    # elif media.lower == "gpr":
    #     #go pro raw file
    #     file_extension = "GPR"
    # elif media.lower == "LVR":
    #     #go pro low resultion file for videos
    #     pass
    # elif media.lower == "thm":
    #     #go pro thumb file images
    #     pass

    images = filter_media(mfm.media, file_extension="JPG")

    for img in images:
        mfm.fetch_file(img)


if __name__ == "__main__":
    gopro_sync_cli()
