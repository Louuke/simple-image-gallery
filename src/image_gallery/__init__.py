from flask import Flask
from flask_injector import FlaskInjector

from image_gallery.configuration.config import GalleryConfig
from image_gallery.configuration.modules import ServiceModule
from image_gallery.controller import index, images


Flask.url_for.__annotations__ = {} # Workaround: https://github.com/python-injector/flask_injector/issues/78

def create_app() -> Flask:
    _app = Flask(__name__)

    _app.config.from_object(GalleryConfig())
    _app.config.from_prefixed_env()

    _app.register_blueprint(index.index_bp)
    _app.register_blueprint(images.images_bp)

    return _app

def setup_injector(_app: Flask):
    FlaskInjector(_app, modules=[ServiceModule])

app = create_app()
setup_injector(app)

