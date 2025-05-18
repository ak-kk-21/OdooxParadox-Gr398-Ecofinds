import os
from flask import Flask

import app.database
print("app.database module:", app.database)
print("init_app attribute:", hasattr(app.database, "init_app"))


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # Change this to a secure random key in production
        DATABASE=os.path.join(app.instance_path, 'marketplace.sqlite'),
        UPLOAD_FOLDER=os.path.join('app', 'static', 'uploads')
    )

    if test_config is None:
        # Load the instance config, if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Hello route (optional sanity check)
    @app.route('/hello')
    def hello():
        return 'Hello World 🌍'

    # Import and register blueprints
    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import browsing
    app.register_blueprint(browsing.bp)

    from . import user_functions
    app.register_blueprint(user_functions.bp)

    # Define the root route (landing page)
    app.add_url_rule('/', endpoint='index')

    return app
