import mimetypes
import random
from datetime import datetime
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Config

from image_gallery.services.base import BaseService


class ImageService(BaseService):

    def __init__(self, config: Config):
        super().__init__(config)
        self._file_extensions = ['jpg', 'jpeg', 'png']

    def get_image_paths(self, sort: int) -> [Path]:
        """
        Gets the paths of all images in the gallery directory and sorts them based on the sort parameter.

        Args:
            sort: 1 for ascending, -1 for descending, 0 for random
        Returns:
            list: sorted list of image paths
        """
        image_paths = self._find_images()
        return self._sort_images(image_paths, sort)

    def paginate_images(self, image_paths: [Path], page: int, items: int) -> [(Path, str)]:
        """
        Paginates the image paths and returns a list of tuples with the image path and its creation time.

        Args:
            image_paths: list of image paths
            page: current page number
            items: number of items per page
        Returns:
            list: paginated list of image paths with their creation time
        """
        start = (page - 1) * items
        end = start + items
        return [(path, self._format_ctime(path)) for path in image_paths[start:end]]

    def create_image_archive(self, filenames: [str]) -> (bytes, str):
        """ Creates an in-memory archive of images specified by their filenames

        Args:
            filenames: list of image filenames
        Returns:
            tuple: zip archive bytes and mime type
        """
        buffer = BytesIO()
        with ZipFile(buffer, 'w', compression=ZIP_DEFLATED) as archive:
            for name in filenames:
                archive.write(f'{self.gallery_directory}/{name}', name)
        return buffer.getvalue(), 'application/zip'

    def read_image(self, filename: str) -> (bytes, str):
        """ Reads the image from the file system and returns it

        Args:
            filename: image filename
        Returns:
            tuple: image bytes and mime type
        """
        path = f'{self.gallery_directory}/{filename}'
        mime_type, _ = mimetypes.guess_type(path)
        with open(path, 'rb') as img:
            return img.read(), mime_type

    def _find_images(self) -> list[Path]:
        gallery_dir = Path(self.gallery_directory)
        paths = []
        for ext in self._file_extensions:
            for img_path in gallery_dir.glob(f'*.{ext}'):
                paths.append(img_path)
        return paths

    def _format_ctime(self, path: Path) -> str:
        time_format = self.gallery_image_date_format
        ctime = path.stat().st_ctime
        date = datetime.fromtimestamp(ctime)
        return date.strftime(time_format)

    @staticmethod
    def _sort_images(image_paths: [Path], sort: int) -> [Path]:
        lst = image_paths.copy()
        match sort:
            case 1:  # Ascending
                lst.sort(key=lambda path: path.stat().st_ctime)
            case -1:  # Descending
                lst.sort(key=lambda path: path.stat().st_ctime, reverse=True)
            case _:  # Random
                random.shuffle(lst)
        return lst

    @property
    def image_archive_name(self) -> str:
        return f'{self.gallery_header}.zip'
