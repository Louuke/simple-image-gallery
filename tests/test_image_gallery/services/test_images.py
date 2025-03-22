import hashlib
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest

from image_gallery.services.images import ImageService


class TestImageService:

    @pytest.fixture()
    def service(self, app) -> ImageService:
        return ImageService(app.config)

    def test_read_image(self, service: ImageService):
        image_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
        for path in image_paths:
            sha256 = calculate_sha256(read_file(path))
            data, mimetype = service.read_image(path.name)
            assert sha256 == calculate_sha256(data)
            assert mimetype is not None
            assert mimetype in ['image/jpeg', 'image/png', 'image/jpg']

    def test_create_image_archive(self, service: ImageService):
        image_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
        filenames = [path.name for path in image_paths]
        archive, mimetype = service.create_image_archive(filenames)
        assert mimetype == 'application/zip'
        with ZipFile(BytesIO(archive)) as zf:
            for path in image_paths:
                with zf.open(path.name) as f:
                    assert calculate_sha256(read_file(path)) == calculate_sha256(f.read())


def calculate_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_file(path: Path) -> bytes:
    with open(path, 'rb') as f:
        return f.read()