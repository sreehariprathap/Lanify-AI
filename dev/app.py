import logging
import os
import sys

# make sure the project directory is in the path
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from flask import Flask

from dev.config import Config
from dev.extensions import db, ma, api, migrate
from dev.service.driving_training_service import blp as driving_training_blp
from dev.service.dashcam_service import blp as dashcam_blp
from dev.service.road_infra_service import blp as road_infra_blp


def create_app():
    app = Flask('Lanify')
    app.config.from_object(Config)
    app.logger.setLevel(logging.INFO)

    app.logger.info(f"API Documentation: http://{Config.APP_HOST}:{Config.APP_PORT}/swagger-ui")

    register_extensions(app)
    register_blueprints()

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)


def register_blueprints():
    api.register_blueprint(driving_training_blp)
    api.register_blueprint(dashcam_blp)
    api.register_blueprint(road_infra_blp)


if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=True)
