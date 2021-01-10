import json
from pathlib import Path
import glob
from datetime import datetime
import subprocess
import sys

EXIFTOOL_PATH = "Image-ExifTool-12.14/exiftool"
FOLDER_PATH = "messages"
FILES_WITH_ERRORS = []
FILES_NOT_FOUND = []

EXIFTOOL_PATH = Path(EXIFTOOL_PATH)

def main():
    read_json_files(FOLDER_PATH)
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


def run_exiftool(exiftool_path, obj, is_video=False):
    arguments = []
    path = obj["uri"]
    if not path.exists():
        print(f"file \"{str(path)}\" does not exist!")
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
        arguments.append("-overwrite_original")
        print(f"Running {' '.join([str(exiftool_path)]+arguments+[str(path)])}")
        try:
            subprocess.run([exiftool_path] + arguments + [path], check=True)
            print(f"Appended exif data succesfully!")
        except Exception as e:
            print(f"exiftool error!")
            FILES_WITH_ERRORS.append(str(path))
            print(e)
    print()


def read_json_files(path):
    path = Path(path).joinpath("**").joinpath("*.json")
    print(f"Reading json files in {str(path)}...")
    for file in glob.iglob(str(path), recursive=True):
        photos, videos, gifs = read_json(file)
        for photo in photos + gifs:
            run_exiftool(EXIFTOOL_PATH, photo)
        for video in videos:
            run_exiftool(EXIFTOOL_PATH, video, is_video=True)


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
