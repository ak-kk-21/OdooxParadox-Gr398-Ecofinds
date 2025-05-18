from flask import Blueprint

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/')
def cart_index():
    return "Cart homepage"
