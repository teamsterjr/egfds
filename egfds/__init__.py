import os

from flask import Flask
from . import db
from . import main
from . import games
from . import admin
from . import utils

__version__='2.0.0'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py")
        app.config.from_pyfile("secret.py")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    admin.init_app(app)
    main.init_app(app)
    utils.init_app(app)

    app.register_blueprint(main.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(admin.bp)

    return app
