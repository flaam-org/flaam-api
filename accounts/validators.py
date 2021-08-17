from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^(?=.{4,32}$)(?![_])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$"
    message = _(
        "Username must be 4 to 32 characters long. "
        "It may only contain letters, numbers and alphabets. "
        "It shouldn't start or end with underscores. "
        "It shouldn't contain consecutive underscores"
    )
    flags = 0
