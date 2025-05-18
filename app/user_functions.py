from flask import Blueprint

bp = Blueprint('user_functions', __name__, url_prefix='/user')

@bp.route('/')
def user_index():
    return "User functions homepage"
