import asyncio
import shutil
import logging


class FileReader:
    def __init__(self, logger):
        self.logger = logger

    async def read_folder(self, source_folder, output_folder):
        self.logger.info(f"Read from folder {source_folder} to {output_folder}")
        for file_path in source_folder.rglob("*"):
            if file_path.is_file():
                await self.copy_file(file_path, output_folder)

    async def copy_file(self, file_path, output_folder):
        try:
            extension = file_path.suffix.lower()
            destination_folder = output_folder / extension[1:]

            destination_folder.mkdir(parents=True, exist_ok=True)

            shutil.copy(file_path, destination_folder)

            self.logger.info(f"Copied {file_path} to {destination_folder}")
        except Exception as e:
            self.logger.error(f"Error occurred while copying {file_path}: {e}")
