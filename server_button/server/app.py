""" App initialization module."""

import logging
from logging.config import dictConfig
from os import path
import yaml
from flask import Flask
from .managers.thread_manager import thread_manager_service
from .managers.mqtt_manager import mqtt_manager_service
from .managers.button_manager import button_manager_service
from .managers.wifi_connection_manager import wifi_connection_manager_service
from .common import ServerButtonException, handle_server_button_exception

logger = logging.getLogger(__name__)


def create_app(
    config_dir: str = path.join(path.dirname(path.abspath(__file__)), "config"),
):
    """Create the Flask app"""

    # Create app Flask
    app = Flask("Server Camera")

    # Get configuration files
    app_config = path.join(config_dir, "server-camera-config.yml")

    logging_config = path.join(config_dir, "logging-config.yml")

    # Load logging configuration and configure flask application logger
    with open(logging_config) as stream:
        dictConfig(yaml.full_load(stream))

    logger.info("App config file: %s", app_config)

    # Load configuration
    app.config.from_file(app_config, load=yaml.full_load)

    # Register extensions
    register_extensions(app)
    logger.info("App ready!!")

    return app


def register_extensions(app: Flask):
    """Initialize all extensions"""

    # MQTT service
    mqtt_manager_service.init_app(app=app)
    # Thread manager extension
    thread_manager_service.init_app(app=app)
    # Button manager extension
    button_manager_service.init_app(app=app)
    # Wifi connection manager extention
    wifi_connection_manager_service.init_app(app=app)

