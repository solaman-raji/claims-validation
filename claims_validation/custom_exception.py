from rest_framework import status
from rest_framework.exceptions import APIException


class DoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Object does not exist.'
    default_code = 'does_not_exist'


class InvalidParameter(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid parameter.'
    default_code = 'invalid_parameter'
