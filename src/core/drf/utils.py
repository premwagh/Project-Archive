from rest_framework.response import Response

def format_success_msg(msg):
    return {"message": msg}

def format_error_msg(msg):
    if isinstance(msg, str):
        msg = [msg]
    return {"detail": msg}

def response_success_msg(msg, status=200):
    return Response(format_success_msg(msg), status=status)

def response_error_msg(msg, status=400):
    return Response(format_error_msg(msg), status=status)