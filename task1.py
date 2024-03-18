import asyncio
import os
import shutil
import argparse
from pathlib import Path


async def copy_file(root, file, destination):
    source_path = Path(root, file)
    extension = os.path.splitext(file)[1]
    destination_folder = Path(destination, extension[1:])

    destination_folder.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy(source_path, destination_folder)
        print(f"File '{file}' copied to '{destination_folder}'.")
    except Exception as e:
        print(f"Error occurred when attempted to copy '{file}': {e}")


async def read_folder(source, destination):
    if not os.path.exists(source):
        print(f"Folder '{source}' does not exist.")
        return

    for root, _, files in os.walk(source):
        for file in files:
            await copy_file(root, file, destination)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help="Source folder path",
        default=r"E:\git\goit-cs-hw-05\source"
    )
    parser.add_argument(
        "--destination",
        type=Path,
        help="Destination folder path",
        default=r"E:\git\goit-cs-hw-05\destination"
    )
    args = parser.parse_args()
    source_folder = args.source
    destination_folder = args.destination

    if not os.path.exists(source_folder):
        print(f"Invalid source folder path: {source_folder}")
        return

    if not os.path.exists(destination_folder):
        print(f"Invalid destination folder path: {destination_folder}. Creating folder...")
        destination_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, destination_folder)


if __name__ == "__main__":
    asyncio.run(main())
