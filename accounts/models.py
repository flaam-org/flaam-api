from django.contrib.auth.models import AbstractUser
from django.db import models

from tags.models import Tag

from .utils import avatar_path
from .validators import UsernameValidator


class User(AbstractUser):
    username = models.CharField(
        error_messages={"unique": "A user with that username already exists."},
        help_text=(
            "Username must be 4 to 32 characters long.\n"
            "It may only contain letters, numbers and alphabets.\n"
            "It shouldn't start or end with underscores.\n"
            "It shouldn't contain consecutive underscores"
        ),
        max_length=32,
        unique=True,
        validators=(UsernameValidator,),
        verbose_name="username",
    )
    email = models.EmailField(
        error_messages={"unique": "A user with that email already exists."},
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True)
    status = models.CharField(
        max_length=20, blank=True, null=True, help_text="A short status message"
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="A short description about the user",
    )
    favourite_tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.username