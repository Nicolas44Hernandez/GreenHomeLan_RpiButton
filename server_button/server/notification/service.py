import logging
from server.managers.thread_manager import thread_manager_service
from flask import Flask

logger = logging.getLogger(__name__)


class AlarmNotifier:
    """Manager for AlarmNotifier"""

    mqtt_alarm_notif_topic: str

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize AlarmNotifier"""
        if app is not None:
            logger.info("initializing the AlarmNotifier")
            self.mqtt_alarm_notif_topic = app.config["MQTT_ALARM_NOTIFICATION_TOPIC"]

    def notify_alarm(self, alarm_type: str, msg: str):
        logger.info(f"Sending emergency alarm notification alarm:{alarm_type} msg:{msg}")
        """Notify alarm to orchestrator"""
        return self.notify_thread_alarm(alarm_type=alarm_type)


    def notify_thread_alarm(self, alarm_type: str) -> bool:
        """Send Thread message to notify alarm"""
        logger.info(f"Sending notification via Thread")

        if alarm_type == "emergency_btn":
            data_to_send = f"al_bt_em"
        else:
            return False
        return thread_manager_service.send_thread_message_to_border_router(data_to_send)


notification_service: AlarmNotifier = AlarmNotifier()
""" AlarmNotifier service singleton"""
