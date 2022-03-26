from flask import jsonify

def api_response(message: str, code: int = 200):
    """Making sure the API return value is unified
    """
    return jsonify(msg=message), code