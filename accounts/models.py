from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.utils.timezone import datetime

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


class PasswordResetToken(models.Model, PasswordResetTokenGenerator):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

    def generate_token(self) -> str:
        return PasswordResetTokenGenerator().make_token(self.user)

    def save(self, *args, **kwargs) -> None:
        self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def is_valid(self) -> bool:
        token_time = self.created_at + settings.PASSWORD_RESET_TOKEN_VALIDITY
        return token_time > datetime.now()
