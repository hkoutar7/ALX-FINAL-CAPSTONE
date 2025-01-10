from rest_framework.response import Response
from datetime import datetime


def generate_response(status_code, message, data=None):
    """
        Helper function to generate consistent API responses.
    """

    return Response({
        'status_code': status_code,
        'message': message,
        'timestamp': datetime.now(),
        'data': data
    }, status=status_code)
