# Generated by Django 3.2.8 on 2021-10-26 08:11

from django.db import migrations, models

import tags.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={"unique": "This Tag already exists."},
                        help_text="Tag name must be 1 to 50 characters long. It may only contain lowercase alphabets, numbers and hyphens. It shouldn't start or end with hyphens. It shouldn't contain consecutive hyphens",
                        max_length=50,
                        unique=True,
                        validators=[tags.validators.TagNameValidator()],
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
