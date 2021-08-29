from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            exc = DRFValidationError(detail=exc.message_dict)
        else:
            exc = DRFValidationError(detail=exc.message)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # response = drf_exception_handler(exc, context)
    # if response is not None:
    #     response.data = {
    #         "message": response.data.get("detail", "Unexpected error occured.")
    #     }
    # return response
    return drf_exception_handler(exc, context)


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "Entity not found."}
    default_code = "not_found"

    def __init__(self, detail=None, code=None):
        self.detail = detail if detail else self.default_detail
        self.code = code if code else self.default_code
