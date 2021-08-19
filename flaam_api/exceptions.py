from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "Entity not found."}
    default_code = "not_found"

    def __init__(self, detail=None, code=None):
        self.detail = detail if detail else self.default_detail
        self.code = code if code else self.default_code
