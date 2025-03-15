from pathlib import Path

from flask import Config
from datetime import datetime

from image_gallery.services.base import BaseService


class IndexService(BaseService):

    def __init__(self, config: Config):
        super().__init__(config)
        self._file_extensions = ['jpg', 'jpeg', 'png']

    def get_image_paths(self, sort: int) -> [Path]:
        image_paths = self._find_images()
        reverse = False if sort == 1 else True
        image_paths.sort(key=lambda path: path.stat().st_ctime, reverse=reverse)
        return image_paths

    def paginate_images(self, image_paths: [Path], page: int, items: int) -> [(str, str)]:
        start = (page - 1) * items
        end = start + items
        return [(path.name, self._format_ctime(path)) for path in image_paths[start:end]]

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
