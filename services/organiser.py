import os
import logging
import calendar
import shutil

from datetime import datetime
from pathlib import Path
from PIL import Image


class OrganiserService:
    source = None
    destination = None

    def __init__(self, source, destination):
        """
        :param source: Source of files to organise
        :param destination: Destination of organised folders
        """
        self.source = source
        self.destination = destination

    def organise_images_by_date(self):
        """
        Loads each file in the source directory using Pillow to find the date taken,
        and then moves this to a folder at destination/year/month/day.
        """
        files = [file for file in os.listdir(self.source) if not os.path.isdir(file)]
        logging.info(f"Discovered {len(files)} files...")

        successful = 0
        failed = 0
        for file in files:
            try:
                img_path = Path.joinpath(self.source, file)
                img = Image.open(img_path)

                date_str = img.getexif().get(306)
                date_taken = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                month_string = f"{date_taken.month:02} {calendar.month_name[date_taken.month]}"

                organised_dest_dir = Path.joinpath(self.destination,
                                                   str(date_taken.year),
                                                   month_string,
                                                   str(date_taken.day))
                organised_dest_file = Path.joinpath(organised_dest_dir, file)

                self._safely_make_dir(organised_dest_dir)
                shutil.copy(img_path, organised_dest_file)
                successful += 1
            except IOError:
                logging.info(f"Failed to load {img_path}, not a valid image.")
                failed += 1

        logging.info(f"Organisation finished. Successfully moved {successful} files. Failed to move {failed} files.")

    def _safely_make_dir(self, path):
        if not os.path.exists(path):
            Path.mkdir(path, parents=True)
