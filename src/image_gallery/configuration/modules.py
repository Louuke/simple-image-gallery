from flask import Config
from injector import Module, provider

from image_gallery.services.images import ImagesService
from image_gallery.services.frontend import FrontendService


class ServiceModule(Module):

    @provider
    def provide_index_service(self, config: Config) -> FrontendService:
        return FrontendService(config)

    @provider
    def provide_images_service(self, config: Config) -> ImagesService:
        return ImagesService(config)