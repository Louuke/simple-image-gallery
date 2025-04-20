from pathlib import Path

import pytest

from simple_image_gallery import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'GALLERY_DIRECTORY': Path(__file__).parent / 'resources', # Path to the test resources
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
