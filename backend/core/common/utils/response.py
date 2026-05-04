def success(data=None):
    return {
        "code": 0,
        "message": "success",
        "data": data
    }


def error(msg="error"):
    return {
        "code": 1,
        "message": msg,
        "data": None
    }

