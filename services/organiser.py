import os
import logging
import calendar
import shutil

from datetime import datetime
from pathlib import Path
from PIL import Image

from services.facial_recognition import FacialRecognitionService

class OrganiserService:
    source = None
    destination = None

    facial_recognition_service = FacialRecognitionService()

    def __init__(self, source, destination):
        """
        :param source: Source of files to organise
        :param destination: Destination of organised folders
        """
        self.source = source
        self.destination = destination

    def organise_images_by_date(self, rename_from_faces):
        """
        Loads each file in the source directory using Pillow to find the date taken,
        and then moves this to a folder at destination/year/month/day.

        :param rename_from_faces: True if you want to use facial recognition to prompt renaming of files
                                    containing faces.
        """
        files = [file for file in os.listdir(self.source) if not os.path.isdir(file)]
        logging.info(f"Discovered {len(files)} files...")

        successful = 0
        failed_count = 0
        failed = []
        with_faces = 0

        for file in files:
            try:
                img_path = Path.joinpath(self.source, file)
                img = Image.open(img_path)

                date_str = img.getexif().get(306)
                date_taken = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                month_string = f"{date_taken.month:02} {calendar.month_name[date_taken.month]}"

                organised_name = file
                if rename_from_faces:
                    contains_face, faces = self.facial_recognition_service.contains_face(str(img_path))
                    if contains_face:
                        with_faces += 1
                        name = self.facial_recognition_service.show_faces_and_get_input(str(img_path), faces)
                        if name:
                            organised_name = f"{name} {date_taken.strftime('%H%M%S')}.{file.split('.')[-1]}"

                organised_dest_dir = Path.joinpath(self.destination,
                                                   str(date_taken.year),
                                                   month_string,
                                                   str(date_taken.day))
                organised_dest_file = Path.joinpath(organised_dest_dir, organised_name)

                logging.info(f"Moving {str(img_path)} to {str(organised_dest_file)}\n")

                self._safely_make_dir(organised_dest_dir)
                shutil.copy(img_path, organised_dest_file)
                successful += 1
            except IOError:
                logging.info(f"Failed to load {img_path}, not a valid image.\n")
                failed.append(str(img_path))
                failed_count += 1

        logging.info(f"Organisation finished. Successfully moved {successful} files. Failed to move {failed_count} files. "
                     f"Found faces in {with_faces}.\n")

        logging.warning("--- FAILURES ---")
        for failed_file in failed:
            logging.warning(failed_file)

    def _safely_make_dir(self, path):
        if not os.path.exists(path):
            Path.mkdir(path, parents=True)
