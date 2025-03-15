from flask import Config
from injector import Module, provider

from image_gallery.services.images import ImagesService
from image_gallery.services.index import IndexService


class ServiceModule(Module):

    @provider
    def provide_index_service(self, config: Config) -> IndexService:
        return IndexService(config)

    @provider
    def provide_images_service(self, config: Config) -> ImagesService:
        return ImagesService(config)