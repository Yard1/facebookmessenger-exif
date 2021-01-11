import json
from pathlib import Path
import glob
from datetime import datetime
import subprocess
import sys
import argparse

#############################
###
### Facebook Messenger EXIF data adder
### Written in Python 3.8.6
###
### Copyright (c) 2021 Antoni Baum (Yard1)
### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
### The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
### usage: messengerexif.py [-h] [-b] [-f] messages exiftool
###
### Given a messages folder downloaded from Facebook, append creation date EXIF
### metadata to images, videos and gifs present. EXIF data is obtained from JSON
### files present in the folder. Uses Exiftool - https://exiftool.org/
###
### positional arguments:
###   messages         Path to the messages folder
###   exiftool         Path to exiftool executable (obtained from
###                    https://exiftool.org/)
###
### optional arguments:
###   -h, --help       show this help message and exit
###   -b, --backup     Backup modified files (Default: False)
###   -f, --fail-fast  Stop execution whenever an error is raised, instead of
###                    continuing (Default: False)
###
#############################

FILES_WITH_ERRORS = []
FILES_NOT_FOUND = []

PARSER = argparse.ArgumentParser(
    description="Given a messages folder downloaded from Facebook, append creation date EXIF metadata to images, videos and gifs present. EXIF data is obtained from JSON files present in the folder. Uses Exiftool - https://exiftool.org/"
)
PARSER.add_argument("messages", metavar="messages", help="Path to the messages folder")
PARSER.add_argument(
    "exiftool",
    metavar="exiftool",
    help="Path to exiftool executable (obtained from https://exiftool.org/)",
)
PARSER.add_argument(
    "-b",
    "--backup",
    action="store_true",
    required=False,
    default=False,
    help="Backup modified files (Default: False)",
)
PARSER.add_argument(
    "-f",
    "--fail-fast",
    action="store_true",
    required=False,
    default=False,
    help="Stop execution whenever an error is raised, instead of continuing (Default: False)",
)

def main():
    print("Starting messengerexif...")
    args = PARSER.parse_args()
    folder_path = Path(args.messages)
    if not folder_path.exists():
        print(f'Path "{str(folder_path)}" does not exist!')
        print("Exiting.")
        sys.exit(1)
    if not folder_path.is_dir():
        print(f'Path "{str(folder_path)}" is not a directory!')
        print("Exiting.")
        sys.exit(1)
    exiftool_path = Path(args.exiftool)
    if not exiftool_path.exists():
        print(f'Path "{str(folder_path)}" does not exist!')
        print("Exiting.")
        sys.exit(1)
    backup = args.backup
    fail_fast = args.fail_fast
    read_json_files(folder_path, exiftool_path, backup=backup, fail_fast=fail_fast)
    if FILES_NOT_FOUND:
        print("The following files were not found:")
        print("\n".join(FILES_NOT_FOUND))
    if FILES_WITH_ERRORS:
        print(
            "The following files had errors and didn't have exif data appened to them:"
        )
        print("\n".join(FILES_WITH_ERRORS))
    if FILES_NOT_FOUND or FILES_WITH_ERRORS:
        print("Exiting.")
        sys.exit(1)
    else:
        print("There were no errors!")
    print("Exiting.")


def run_exiftool(exiftool_path, obj, is_video=False, backup=False, fail_fast=False):
    arguments = []
    path = obj["uri"]
    if not path.exists():
        print(f'file "{str(path)}" does not exist!')
        FILES_NOT_FOUND.append(str(path))
    else:
        if is_video:
            arguments.append("-api")
            arguments.append("quicktime")
            arguments.append(f"-CreationDate=\"{obj['creation_timestamp']}\"")
            arguments.append(f"-dateTimeOriginal=\"{obj['creation_timestamp']}\"")
            arguments.append(f"-CreateDate=\"{obj['creation_timestamp']}\"")
            arguments.append(f"-ModifyDate=\"{obj['creation_timestamp']}\"")
            arguments.append(f"-TrackCreateDate=\"{obj['creation_timestamp']}\"")
        arguments.append(f"-CreationDate=\"{obj['creation_timestamp']}\"")
        arguments.append(f"-dateTimeOriginal=\"{obj['creation_timestamp']}\"")
        if not backup:
            arguments.append("-overwrite_original")
        print(f"Running {' '.join([str(exiftool_path)]+arguments+[str(path)])}")
        try:
            subprocess.run([exiftool_path] + arguments + [path], check=True)
            print(f"Appended exif data succesfully!")
        except Exception as e:
            print(f"exiftool error!")
            if fail_fast:
                sys.exit(1)
            FILES_WITH_ERRORS.append(str(path))
            print(e)
    print()


def read_json_files(path, exiftool_path, backup=False, fail_fast=False):
    path = Path(path).joinpath("**").joinpath("*.json")
    print(f"Reading json files in {str(path)}...")
    for file in glob.iglob(str(path), recursive=True):
        photos, videos, gifs = read_json(file)
        for photo in photos + gifs:
            run_exiftool(exiftool_path, photo, backup=backup, fail_fast=fail_fast)
        for video in videos:
            run_exiftool(exiftool_path, video, is_video=True, backup=backup, fail_fast=fail_fast)


def normalize_json(meta, timestamp=None):
    for obj in meta:
        if "creation_timestamp" not in obj:
            if timestamp:
                obj["creation_timestamp"] = timestamp
            else:
                raise ValueError(f"{obj} is lacking creation_timestamp!")
        obj["creation_timestamp"] = int(str(obj["creation_timestamp"])[0:10])
        obj["creation_timestamp"] = datetime.fromtimestamp(
            obj["creation_timestamp"]
        ).strftime("%Y:%m:%d %H:%M:%S")
        obj["uri"] = Path(obj["uri"])
    return meta


def read_json(path):
    print(f"Reading file {path}...")
    with open(path, "r") as f:
        json_file = json.load(f)
    messages = json_file["messages"]
    photos = []
    videos = []
    gifs = []
    for x in [
        normalize_json(x["photos"], x["timestamp_ms"])
        for x in messages
        if "photos" in x
    ]:
        photos.extend(x)
    for x in [
        normalize_json(x["videos"], x["timestamp_ms"])
        for x in messages
        if "videos" in x
    ]:
        videos.extend(x)
    for x in [
        normalize_json(x["gifs"], x["timestamp_ms"]) for x in messages if "gifs" in x
    ]:
        gifs.extend(x)
    print(f"Found {len(photos)} photos, {len(videos)} videos and {len(gifs)} gifs.\n")
    return photos, videos, gifs


if __name__ == "__main__":
    main()
