from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from simple_image_gallery.services.base import BaseService
from simple_image_gallery.utils import time


@pytest.fixture()
def service(app) -> BaseService:
    return BaseService(app.config)


def test_format_ctime_american(service: BaseService):
    file_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
    for path in file_paths:
        date_format = '%m/%d/%Y'
        tz = ZoneInfo('UTC')
        date = datetime.fromtimestamp(path.stat().st_ctime, tz=tz)
        assert f'{date.month:02}/{date.day:02}/{date.year}' == time.format_ctime(path, date_format, tz)


def test_format_ctime_european(service: BaseService):
    file_paths = [path for path in Path(service.gallery_directory).glob('*.*')]
    for path in file_paths:
        date_format = '%d.%m.%Y'
        tz = ZoneInfo('UTC')
        date = datetime.fromtimestamp(path.stat().st_ctime, tz=tz)
        assert f'{date.day:02}.{date.month:02}.{date.year}' == time.format_ctime(path, date_format, tz)
