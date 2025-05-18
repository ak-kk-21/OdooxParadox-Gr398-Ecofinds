from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

bp = Blueprint('browsing', __name__, url_prefix='/browse')

@bp.route('/')
def browse_index():
    return "Browsing homepage"
@bp.route('/landing')
def landing():
    return render_template('browsing/landing.html')
