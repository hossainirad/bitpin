from rest_framework import status

from utils.api.error_objects import ErrorObject
from utils.api.responses import error_response


class BadRequestSerializerMixin:
    @staticmethod
    def serializer_error_response(serializer, extra_error_dict={}):
        error_obj = {
            **ErrorObject.BAD_REQUEST,
            'params': [{'field_name': k, 'field_error': v[0]} for k, v in serializer.errors.items()],
            **extra_error_dict,
        }
        return error_response(error=error_obj, status_code=status.HTTP_400_BAD_REQUEST)
