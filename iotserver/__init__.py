import os

from flask import Flask
from secrets import token_hex


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=token_hex(100),
        DATABASE=os.path.join(app.instance_path, 'iotserver.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app_db(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import panel
    app.register_blueprint(panel.bp)

    from . import api
    app.register_blueprint(api.bp)

    return app
