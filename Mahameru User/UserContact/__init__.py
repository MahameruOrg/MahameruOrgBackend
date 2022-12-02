import os
from flask import Flask
from . import db
from . import user, contacts

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.cfg', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(user.bp)
    app.register_blueprint(contacts.bp)


    @app.route('/')
    def index():
        print("test")
        return "Mahameru Chat"

    return app