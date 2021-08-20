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


class PasswordValidator(validators.RegexValidator):
    regex = r"^(?=.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).*$"
    message = _(
        "Password must be 8 to 32 characters long. "
        "It must contain at least one uppercase letter, "
        "one lowercase letter, one number and one special character."
    )
    flags = 0
