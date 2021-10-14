from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator, avatar_validator


class User(AbstractUser):
    username = models.CharField(
        error_messages={"unique": "A user with that username already exists."},
        help_text=(
            "Username must be 4 to 15 characters long.\n"
            "It may only contain lowercase alphabets, numbers and underscores.\n"
            "It shouldn't start or end with underscores.\n"
            "It shouldn't contain consecutive underscores"
        ),
        max_length=32,
        unique=True,
        validators=(UsernameValidator(),),
        verbose_name="username",
    )
    email = models.EmailField(
        error_messages={"unique": "A user with that email already exists."},
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    show_email = models.BooleanField(default=False)
    avatar = models.CharField(
        max_length=2048, blank=True, null=True, validators=[avatar_validator]
    )
    status = models.CharField(
        max_length=20, blank=True, null=True, help_text="A short status message"
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="A short description about the user",
    )
    following = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="followers"
    )
    favourite_tags = models.ManyToManyField(
        "tags.Tag", blank=True, related_name="favorited_by"
    )
    bookmarked_ideas = models.ManyToManyField(
        "ideas.Idea", blank=True, related_name="bookmarked_by"
    )
    bookmarked_implementations = models.ManyToManyField(
        "implementations.Implementation", blank=True, related_name="bookmarked_by"
    )

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = f"https://avatars.dicebear.com/api/identicon/{self.email}.svg"
        super().save(*args, **kwargs)
