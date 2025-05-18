import os
import re
import sqlite3
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.database import get_db

# This file handles user authentication, including signup and login functionalities.
# It uses Flask's Blueprint to organize the routes and handlers for authentication.

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Email regex (simple version)
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def allowed_file(filename):
    allowed_ext = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        profile_picture = request.files.get('profile_picture')

        # Basic validations
        if not username or len(username) < 3:
            error = 'Username must be at least 3 characters.'
        elif not email or not EMAIL_REGEX.match(email):
            error = 'Invalid email address.'
        elif not password or len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif profile_picture and not allowed_file(profile_picture.filename):
            error = 'Profile picture must be an image (png, jpg, jpeg, gif).'

        if error is None:
            db = get_db()
            # Check if username or email already exists
            user_exists = db.execute(
                'SELECT 1 FROM Users WHERE username = ? OR email = ?', (username, email)
            ).fetchone()
            if user_exists:
                error = 'Username or email already registered.'

        if error is None:
            # Save profile picture
            profile_pic_path = None
            if profile_picture:
                filename = secure_filename(profile_picture.filename)
                upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                profile_picture.save(filepath)
                # Store relative path for DB, e.g. 'static/uploads/filename'
                profile_pic_path = os.path.join('static', 'uploads', filename).replace('\\', '/')

            # Insert user into DB with hashed password
            password_hash = generate_password_hash(password)

            db.execute(
                'INSERT INTO Users (username, email, password_hash, Profile_picture) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, profile_pic_path)
            )
            db.commit()

            flash('Successfully registered! Please login.', 'success')
            return redirect(url_for('auth.login'))

        flash(error, 'error')

    return render_template(r'auth\signup.html', error=error)

# Database helper function to get DB connection
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email_or_username = request.form['email']
        password = request.form['password']

        if not email_or_username or not password:
            error = 'All fields are required.'
        else:
            db = get_db()
            user = db.execute(
                'SELECT * FROM Users WHERE email = ? OR username = ?',
                (email_or_username, email_or_username)
            ).fetchone()

            if user is None:
                error = 'No account found with that email or username.'
            elif not check_password_hash(user['password_hash'], password):
                error = 'Incorrect password.'
            else:
                session.clear()
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                return redirect(url_for('user_functions.dashboard'))

    return render_template(r'auth\login.html', error=error)
