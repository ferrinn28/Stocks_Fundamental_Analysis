def api_response(code=200, success=True, message="", data={}):

    API_RESPONSE = {
        "code": code,
        "success": success,
        "message": message,
        "data": data
    }

    return API_RESPONSE