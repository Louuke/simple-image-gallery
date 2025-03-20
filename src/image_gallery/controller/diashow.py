from flask import Blueprint, render_template, request

from image_gallery.services.images import ImageService

diashow_bp = Blueprint('diashow', __name__)


@diashow_bp.get('/diashow')
def diashow(service: ImageService):
    # Get query parameters
    sort = request.args.get('sort', 0, int)
    # Get image paths
    image_paths = service.get_image_paths(sort)
    # Render the template
    template_vars = {
        'sort': sort,
        'images': image_paths
    }
    return render_template('diashow.html', **template_vars)