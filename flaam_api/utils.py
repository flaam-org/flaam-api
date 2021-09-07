from rest_framework.pagination import LimitOffsetPagination


def errors_to_string(errors: dict) -> str:
    """
    A function to flaten out the default error object from serializer classes
    to a string
    """
    error_string = []
    for _, error in errors.items():
        error_string.append(error[0])
    return "\n".join(error_string)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    A custom pagination class
    """

    default_limit = 10
    max_limit = 30
