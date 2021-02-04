def build_error(message, details = {}, **kwargs):

    error = {"error": message}

    if details:
        error["details"] = details

    if len(kwargs):
        error["details"] = {}

    for key, value in kwargs.items():
        error['details'][key] = value

    return error