import logging
import time
from datetime import timedelta
from timeloop import Timeloop
from flask import Flask
from server.interfaces.battery_interface import BatteryInterface
from server.managers.thread_manager import thread_manager_service

logger = logging.getLogger(__name__)

battery_status_timeloop = Timeloop()

class BatteryManager:
    """Manager for Batery"""

    batery_interface: BatteryInterface
    battery_polling_period_in_sec: int
    low_battery_threshold_in_percentage: int
    device_id: str

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize BatteryManager"""
        if app is not None:
            logger.info("initializing the BatteryManager")

            self.batery_interface = BatteryInterface()
            self.battery_polling_period_in_mins = app.config["PIJUICE_BAT_POLLING_PERIOD_IN_MINS"]
            self.low_battery_threshold_in_percentage = app.config["PIJUICE_LOW_BAT_THRESHOLD_IN_PERCENTAGE"]
            self.device_id = app.config["PIJUICE_DEVICE_ID"]

            # Set polling task
            self.schedule_battery_status_polling()

    def schedule_battery_status_polling(self):
        """Schedule the battery status polling"""

        # Battery status polling job
        @battery_status_timeloop.job(interval=timedelta(minutes=self.battery_polling_period_in_mins))
        def check_battery_level():
            logger.info(f"Launch battery status polling")
            bat_level = self.batery_interface.get_battery_level()
            self.send_battery_level(bat_level)
            time.sleep(2)
            if bat_level <= self.low_battery_threshold_in_percentage:
                self.send_low_battery_alarm()

        battery_status_timeloop.start(block=False)


    def send_battery_level(self, battery_level: int):
        logger.info(f"Sending battery level")
        """Send battery level"""
        msg = f"bt_{self.device_id}_{battery_level}"
        thread_manager_service.send_thread_message_to_border_router(message=msg)

    def send_low_battery_alarm(self):
        logger.info(f"Sending battery level alarm")
        """send low battery alarm"""
        msg = f"al_bt{self.device_id}_bat"
        thread_manager_service.send_thread_message_to_border_router(message=msg)

battery_manager_service: BatteryManager = BatteryManager()
""" Battery manager service singleton"""
