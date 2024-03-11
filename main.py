import argparse
import asyncio
import logging
from pathlib import Path
from Task_1 import FileReader


async def main():
    parser = argparse.ArgumentParser(description="Sorting files")
    parser.add_argument("--source", "-s", required=True, help="Source dir")
    parser.add_argument("--output", "-o", help="Output dir", default="destination")
    args = vars(parser.parse_args())
    source_folder = Path(args["source"])
    output_folder = Path(args["output"])

    # You can hardcode a source, just comment all parser instances
    # Hardcoded path source = Path(".\\files\\")
    # source_folder = Path(".\\files\\")
    # You can hardcode an output, just comment all parser instances
    # Hardcoded path output = Path(".\\output\\")
    # output_folder = Path(".\\output\\")

    logger = logging.getLogger(__name__)
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logger.addHandler(logging.FileHandler(filename="logs.log"))

    if not source_folder.exists():
        self.logger.error(f"Source folder '{source_folder}' does not exist.")
        return

    file_reader = FileReader(logger)
    await file_reader.read_folder(source_folder, output_folder)

    logging.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
