"""
Va a verificar si el usuario tiene una cookie
"""

from flask import *

check = Blueprint('check', __name__)

@check.route("/check/session", methods=["GET"])
def main():
    if len(session):
        response = make_response(session.get("username"))
        response.status_code = 200
        return response
    
    abort(401)
