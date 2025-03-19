from flask import Blueprint, send_from_directory, request, Response

from image_gallery.services.images import ImagesService

images_bp = Blueprint('images', __name__, url_prefix='/images')


@images_bp.get('/<filename>')
def send_image(filename: str, service: ImagesService):
    # Returns an image from the gallery directory
    return send_from_directory(service.gallery_directory, filename)


@images_bp.post('')
def download_images(service: ImagesService):
    # Allows downloading a single image or a zip archive of multiple images
    images = list(request.form.keys())
    match len(images):
        case 0:  # No images selected
            return Response('No images selected', status=400)
        case 1:  # Return the image directly
            data, mimetype = service.read_image(images[0])
            filename = images[0]
        case _:  # Create a zip archive
            data, mimetype = service.create_image_archive(images)
            filename = service.image_archive_name
    return Response(data, mimetype=mimetype, headers={'Content-Disposition': f'attachment; filename={filename}'})
