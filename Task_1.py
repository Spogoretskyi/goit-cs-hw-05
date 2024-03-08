import asyncio
import os
import shutil
import logging
from argparse import ArgumentParser


async def read_folder(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            await copy_file(os.path.join(root, file))


async def copy_file(file_path):
    try:
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        destination_folder = os.path.join(
            output_folder, extension[1:]
        )  # ignoring the dot in extension

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copy(file_path, destination_folder)
        print(f"Copied {file_path} to {destination_folder}")
    except Exception as e:
        logging.error(f"Error occurred while copying {file_path}: {e}")


async def main():
    parser = ArgumentParser(
        description="Sort files based on their extensions asynchronously"
    )
    parser.add_argument(
        "source_folder", help="Source folder containing files to be sorted"
    )
    parser.add_argument("output_folder", help="Output folder to store sorted files")
    args = parser.parse_args()

    global output_folder
    output_folder = args.output_folder

    if not os.path.exists(args.source_folder):
        print(f"Source folder '{args.source_folder}' does not exist.")
        return
    await read_folder(args.source_folder)


if __name__ == "__main__":
    logging.basicConfig(filename="error.log", level=logging.ERROR)
    asyncio.run(main())
