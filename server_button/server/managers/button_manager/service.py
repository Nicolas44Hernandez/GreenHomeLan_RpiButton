import logging
import time
import yaml
from flask import Flask
from server.interfaces.gpio_interface import GpioButtonInterface
from server.managers.wifi_connection_manager import wifi_connection_manager_service
from server.managers.thread_manager import thread_manager_service
from server.common import ServerButtonException, ErrorCode


logger = logging.getLogger(__name__)


class ButtonManager:
    """Manager for Button peripheral"""

    gpio_interface: GpioButtonInterface
    thread_commands = {}

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize ButtonManager"""
        if app is not None:
            logger.info("initializing the ButtonManager")

            self.load_thread_messages(app.config["THREAD_MESSAGES"])
            self.gpio_interface = GpioButtonInterface(
                button_pin=app.config["PERIPHERALS_BUTTON"],
                callback_function=self.button_press_callback,
            )

    def load_thread_messages(self, thread_yaml_file: str):
        """Load the thread messages dict from file"""
        logger.info("Thread messages file: %s", thread_yaml_file)

        with open(thread_yaml_file) as stream:
            try:
                self.thread_commands = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ServerButtonException(ErrorCode.THREAD_MESSAGES_FILE_ERROR)

    def button_press_callback(self, channel):
        """Callback function for button press"""
        # Button debounce
        time.sleep(0.2)
        logger.info("Button pressed")

        # If Wifi if not active, send thread command to activate it
        if not wifi_connection_manager_service.connected:
            # wifi_on_command = self.wifi_thread_commands["WIFI"]["BANDS"]["5GHz"][True]
            logger.info(f"Not connected to Wifi")
            #thread_manager_service.send_thread_message_to_border_router(wifi_on_command)
            #self.set_wifi_off_timer()
        else:
            logger.info("Already connected to Wifi")


button_manager_service: ButtonManager = ButtonManager()
""" Button manager service singleton"""
