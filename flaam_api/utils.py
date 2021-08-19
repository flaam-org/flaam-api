from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "message": response.data.get("detail", "Unexpected error occured.")
        }
    return response


def errors_to_string(errors: dict) -> str:
    """
    A function to flaten out the default error object from serializer classes
    to a string
    """
    error_string = []
    for _, error in errors.items():
        error_string.append(error[0])
    return "\n".join(error_string)
