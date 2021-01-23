from flask import jsonify

def build_error(message, details = {}, **kwargs):

    error = {"error": error}

    if details:
        error["details"] = details

    if len(kwargs):
        error["details"] = {}

    for key, value in kwargs:
        error['details'][key] = value

    return error