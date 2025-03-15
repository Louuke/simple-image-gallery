from flask import Blueprint, render_template

diashow_bp = Blueprint('diashow', __name__, url_prefix='/diashow')


@diashow_bp.get('')
def diashow():
    return render_template('diashow.html')