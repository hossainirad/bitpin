from rest_framework import status
from rest_framework.response import Response


def success_response(data: dict, status_code: int = status.HTTP_200_OK) -> Response:
    response_data = {
        'success': True,
        'data': data,
    }
    return Response(response_data, status_code, content_type='application/json')


def error_response(error: dict, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    response_data = {
        'success': False,
        'error': error,
    }
    return Response(response_data, status_code, content_type='application/json')

