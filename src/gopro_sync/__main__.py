import logging

from rich.logging import RichHandler

from gopro_sync.cli import gopro_sync_cli

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[RichHandler()],
)

if __name__ == "__main__":
    gopro_sync_cli()
