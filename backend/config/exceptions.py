from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Equivalent of middlewares/error.js -> errorMiddleware.
    Normalizes every error response to { success: false, message: "..." }.
    """
    response = exception_handler(exc, context)

    if response is not None:
        message = response.data
        if isinstance(message, dict):
            # DRF puts validation errors / detail under different keys;
            # collapse them into one readable message string.
            if "detail" in message:
                message = str(message["detail"])
            else:
                first_key = next(iter(message))
                val = message[first_key]
                val = val[0] if isinstance(val, list) else val
                message = f"{first_key}: {val}" if first_key != "non_field_errors" else str(val)
        elif isinstance(message, list):
            message = str(message[0])

        response.data = {"success": False, "message": message}
        return response

    # Unhandled exceptions -> 500, matching err.statusCode || 500
    return Response({"success": False, "message": str(exc) or "Internal Server Error"}, status=500)
