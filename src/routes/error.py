def build_error(message, code = "SRV01", details = {}, **kwargs):

    error = {"error": message,
             "code": code}

    if details:
        error["details"] = details

    if len(kwargs):
        error["details"] = {}

    for key, value in kwargs.items():
        error['details'][key] = value

    return error