""" Exception handler module for REST API """

from flask import jsonify
from .model import ServerButtonException


def handle_server_button_exception(ex: ServerButtonException):
    """Customize returned body"""

    # Create error response
    response = {
        "code": ex.http_code,
        "status": ex.message,
        "ExceptionCode": ex.code,
    }
    return jsonify(response), ex.http_code
