from datetime import datetime
from pathlib import Path

import pytest

from image_gallery.services.base import BaseService
from image_gallery.utils import time


@pytest.fixture()
def service(app) -> BaseService:
    return BaseService(app.config)


def test_format_ctime_american(service: BaseService):
    file_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
    for path in file_paths:
        date_format = '%m/%d/%Y'
        date = datetime.fromtimestamp(path.stat().st_ctime)
        assert f'{date.month:02}/{date.day:02}/{date.year}' == time.format_ctime(path, date_format)


def test_format_ctime_european(service: BaseService):
    file_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
    for path in file_paths:
        date_format = '%d.%m.%Y'
        date = datetime.fromtimestamp(path.stat().st_ctime)
        assert f'{date.day:02}.{date.month:02}.{date.year}' == time.format_ctime(path, date_format)
