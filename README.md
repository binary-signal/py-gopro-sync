# py-gopro-sync
Python CLI to sync media files from GoPro cameras via wifi
py-gopro-sync

# Installation



Pipx (recommended)
```shell
pipx install git+https://github.com/binary-signal/py-gopro-sync.git
```

 Pip
 ```shell
 pip install git+https://github.com/binary-signal/py-gopro-sync.git
 ```
 

Poetry
```shell
 poetry add "git+https://github.com/binary-signal/py-gopro-sync.git"
 ```
 
 TODO: release package to pypi


# Cli Help

```shell
❯ gopro-sync --help
Usage: gopro-sync [OPTIONS]

  Sync gopro media file via wifi.

  Select `media_type` to sync

Options:
  -m, --media-type [image|raw-image|video|all]
                                  Media type to sync  [required]
  --sync-path PATH                Export files to local  path  [default:
                                  gopro-media]
  --skip-lowres BOOLEAN           Skip low resolution files  [default: True]
  --help                          Show this message and exit.
  ```
 
 # How to
 
 Assumes you have already connected your local computer somehow how to the go pro wifi!
 
 ## Sync images
 ```shell
 gopro-sync -m image
 ```
 
 ## Sync raw images
 ```shell
 gopro-sync -m raw-image
 ```
 
 ## Sync videos
 ```shell
 gopro-sync -m video
 ```
 
 ## Sync all media files
 ```shell
 gopro-sync -m all
 ```
 Last command will sync all files
