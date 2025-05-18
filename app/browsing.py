from flask import Blueprint

bp = Blueprint('browsing', __name__, url_prefix='/browse')

@bp.route('/')
def browse_index():
    return "Browsing homepage"
