import logging
import os
import sys
import eventlet
from flask import Flask
from flask_socketio import SocketIO

# Make sure the project directory is in the path
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from dev.config import Config
from dev.extensions import db, ma, api, migrate
from dev.service.driving_training_service import blp as driving_training_blp
from dev.service.dashcam_service import blp as dashcam_blp
from dev.service.road_infra_service import blp as road_infra_blp

# Initialize SocketIO globally
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask('Lanify')
    app.config.from_object(Config)
    app.logger.setLevel(logging.INFO)

    app.logger.info(f"API Documentation: http://{Config.APP_HOST}:{Config.APP_PORT}/swagger-ui")

    register_extensions(app)
    register_blueprints()

    # Attach SocketIO to the app
    socketio.init_app(app)

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


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    socketio.emit("alertEvent", {"message": "Welcome! You are connected."})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


# Emit periodic test events
def send_periodic_events():
    while True:
        socketio.emit("alertEvent", {"message": "New event from Flask!"})
        eventlet.sleep(5)


# Start emitting events in a background thread
eventlet.spawn(send_periodic_events)


if __name__ == '__main__':
    app = create_app()
    # socketio.run(app, host="0.0.0.0", port=5173, debug=True)
    socketio.run(app, host=Config.APP_HOST, port=Config.APP_PORT, debug=True)
