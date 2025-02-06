import os
import sys

# make sure the project directory is in the path
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from flask import Flask

from dev.config import Config
from dev.extensions import db, ma, api, migrate
from dev.service.ml_service import blp as ml_blp


def create_app():
    app = Flask('Lanify')
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints()

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)


def register_blueprints():
    api.register_blueprint(ml_blp)


if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=True)
