import argparse
import asyncio
import logging
import requests
from pathlib import Path
from Task_1 import FileReader
from Task_2 import TextAnalyzer


async def read_folder(logger, source_folder, output_folder):
    if not source_folder.exists():
        self.logger.error(f"Source folder '{source_folder}' does not exist.")
        return

    file_reader = FileReader(logger)
    await file_reader.read_folder(source_folder, output_folder)


async def get_text_from_url(logger, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error occurred during fetching text from URL: {e}")
        return None


async def visualize_top_words(logger, url, num_words):
    text_analyzer = TextAnalyzer(logger)
    text = await get_text_from_url(logger, url)
    await text_analyzer.visualize_top_words(text, num_words)


async def main():
    logger = logging.getLogger(__name__)
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logger.addHandler(logging.FileHandler(filename="logs.log"))

    # You can hardcode a source, just comment all parser instances
    # Hardcoded path source = Path(".\\files\\")
    # source_folder = Path(".\\files\\")
    # You can hardcode an output, just comment all parser instances
    # Hardcoded path output = Path(".\\output\\")
    # output_folder = Path(".\\output\\")
    # You can hardcode an URL, just comment all parser instances
    # Hardcoded an url = "<https://gutenberg.net.au/ebooks01/0100021.txt>"
    # You can hardcode a num_words, just comment all parser instances
    # Hardcoded an num_words = 10

    parser = argparse.ArgumentParser(description="Tasks")
    parser.add_argument("--source", "-s", help="Source directory")
    parser.add_argument(
        "--output", "-o", help="Output directory", default="Destination directory"
    )
    parser.add_argument("--url", "-u", help="URL to fetch text")
    parser.add_argument(
        "--num_words",
        "-n",
        type=int,
        default=10,
        help="Number of top words to visualize",
    )
    args = vars(parser.parse_args())

    if args.get("source") is not None:
        source_folder = Path(args["source"])
    else:
        source_folder = ""

    if args.get("output") is not None:
        output_folder = Path(args["output"])
    else:
        output_folder = ""

    if args.get("url") is not None:
        url = args["url"]
    else:
        url = ""

    if args.get("num_words") is not None:
        num_words = args["num_words"]

    if source_folder and output_folder:
        await read_folder(logger, source_folder, output_folder)

    if url:
        await visualize_top_words(logger, url, num_words)

    logging.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
