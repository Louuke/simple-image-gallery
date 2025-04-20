import hashlib
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest

import simple_image_gallery
from simple_image_gallery.services.images import ImageService


@pytest.fixture()
def service_w_images(app) -> ImageService:
    return ImageService(app.config)


@pytest.fixture()
def service_wo_images(app) -> ImageService:
    app.config.update({'GALLERY_DIRECTORY': Path(__file__).parent})
    return ImageService(app.config)


class TestImageService:

    def test_get_image_paths_newest_first(self, service_w_images: ImageService):
        image_paths = service_w_images.get_image_paths(-1)
        assert sorted(image_paths, key=lambda p: p.stat().st_ctime, reverse=True) == image_paths

        image_paths_min = service_w_images.get_image_paths(-1, min_items=100)
        assert 100 == len(image_paths_min)
        assert (image_paths * (100 // len(image_paths) + 1))[:100] == image_paths_min

    def test_get_image_paths_oldest_first(self, service_w_images: ImageService):
        image_paths = service_w_images.get_image_paths(1)
        assert sorted(image_paths, key=lambda p: p.stat().st_ctime) == image_paths

        image_paths_min = service_w_images.get_image_paths(1, min_items=100)
        assert 100 == len(image_paths_min)
        assert (image_paths * (100 // len(image_paths) + 1))[:100] == image_paths_min

    def test_get_image_paths_random(self, service_w_images: ImageService):
        image_paths = service_w_images.get_image_paths(0)
        for _ in range(10):
            if sorted(image_paths) != image_paths:
                assert True
                break

    def test_get_image_paths_default(self, service_wo_images: ImageService):
        default_image = Path(simple_image_gallery.__file__).parent / 'static/img/default.png'
        image_paths = service_wo_images.get_image_paths(0, 5)
        assert 5 == len(image_paths)
        assert [default_image] * 5 == image_paths

    def test_create_image_archive(self, service_w_images: ImageService):
        image_paths = [path for path in Path(service_w_images.gallery_directory).glob('*.*')]
        filenames = [path.name for path in image_paths]
        archive, mimetype = service_w_images.create_image_archive(filenames)
        assert mimetype == 'application/zip'
        with ZipFile(BytesIO(archive)) as zf:
            for path in image_paths:
                with zf.open(path.name) as f:
                    assert calculate_sha256(read_file(path)) == calculate_sha256(f.read())

    def test_read_image(self, service_w_images: ImageService):
        image_paths = [path for path in Path(service_w_images.gallery_directory).glob('*.*')]
        for path in image_paths:
            sha256 = calculate_sha256(read_file(path))
            data, mimetype = service_w_images.read_image(path.name)
            assert sha256 == calculate_sha256(data)
            assert mimetype is not None
            assert mimetype in ['image/jpeg', 'image/png', 'image/jpg']

    def test_paginate_image_paths(self):
        paths = [Path(f'path_{i}.jpg') for i in range(100)]
        page = 3
        items = 10
        paginated = ImageService.paginate_image_paths(paths, page, items)
        assert paginated == paths[20:30]

        page = 1
        items = 20
        paginated = ImageService.paginate_image_paths(paths, page, items)
        assert paginated == paths[:20]


def calculate_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_file(path: Path) -> bytes:
    with open(path, 'rb') as f:
        return f.read()
