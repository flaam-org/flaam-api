# Generated by Django 3.2.6 on 2021-08-18 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tags", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Idea",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=500)),
                ("body", models.TextField()),
                ("draft", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "downvotes",
                    models.ManyToManyField(
                        related_name="downvotes", to=settings.AUTH_USER_MODEL
                    ),
                ),
                ("tags", models.ManyToManyField(to="tags.Tag")),
                (
                    "upvotes",
                    models.ManyToManyField(
                        related_name="upvotes", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "views",
                    models.ManyToManyField(
                        related_name="views", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]