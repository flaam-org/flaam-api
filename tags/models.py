from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "This Tag already exists."},
    )
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
