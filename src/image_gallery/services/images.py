import mimetypes
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Config

from image_gallery.services.base import BaseService


class ImagesService(BaseService):

    def __init__(self, config: Config):
        super().__init__(config)

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

    @property
    def image_archive_name(self) -> str:
        return f'{self.gallery_header}.zip'
