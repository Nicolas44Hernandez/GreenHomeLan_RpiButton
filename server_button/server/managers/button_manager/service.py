import logging
import time
from flask import Flask
from server.interfaces.gpio_interface import GpioButtonInterface
from server.managers.wifi_connection_manager import wifi_connection_manager_service
from server.notification import notification_service

logger = logging.getLogger(__name__)


class ButtonManager:
    """Manager for Button peripheral"""

    gpio_interface: GpioButtonInterface
    therad_messages = {}

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize ButtonManager"""
        if app is not None:
            logger.info("initializing the ButtonManager")

            self.gpio_interface = GpioButtonInterface(
                button_pin=app.config["PERIPHERALS_BUTTON"],
                callback_function=self.button_press_callback,
            )

    def button_press_callback(self, channel):
        """Callback function for button press"""
        # Button debounce
        time.sleep(0.5)
        logger.info("Button button pressed")

        # Notify the alarm to orchestrator
        notification_service.notify_alarm(alarm_type="emergency", msg="button pressed")

button_manager_service: ButtonManager = ButtonManager()
""" Button manager service singleton"""
