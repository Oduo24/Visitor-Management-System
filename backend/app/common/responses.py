from flask import jsonify


def success(data=None, message="Success", status_code=200):
    return (
        jsonify({
            "success": True,
            "message": message,
            "data": data,
        }),
        status_code,
    )


def error(message="An error occurred", status_code=400, errors=None):
    return (
        jsonify({
            "success": False,
            "message": message,
            "errors": errors,
        }),
        status_code,
    )