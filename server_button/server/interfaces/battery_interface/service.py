"""
Pijuice battery interface service
"""
import logging
import time
from pijuice import PiJuice

logger = logging.getLogger(__name__)


class BatteryInterface:
    """Service class for Pijuice Battery management"""

    pijuice_battery: PiJuice

    def __init__(self):

        logger.info(f"Creating Pijuice Battery interface:")
        self.pijuice_battery = PiJuice(1, 0x14) # Instantiate PiJuice interface object

    def get_battery_level(self)-> int:
        """Returns pijuice battery level"""
        bat_level = self.pijuice_battery.status.GetChargeLevel()["data"]
        logger.info(f"Battery level: {bat_level}")
        return int(bat_level)
