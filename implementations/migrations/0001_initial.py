# Generated by Django 3.2.8 on 2021-10-25 15:35

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ideas", "0001_initial"),
        ("tags", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Implementation",
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
                ("description", models.TextField(blank=True, max_length=500)),
                ("body", models.TextField(blank=True)),
                ("repo_url", models.URLField(blank=True)),
                ("draft", models.BooleanField(default=True)),
                ("is_validated", models.BooleanField(default=False)),
                ("is_accepted", models.BooleanField(default=False)),
                (
                    "completed_milestones",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=10),
                        blank=True,
                        default=list,
                        size=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "downvotes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="downvoted_implementations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "idea",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="implementations",
                        to="ideas.idea",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="implementations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="implementation_tags", to="tags.Tag"
                    ),
                ),
                (
                    "upvotes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="upvoted_implementations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "views",
                    models.ManyToManyField(
                        blank=True,
                        related_name="viewed_implementations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ImplementationComment",
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
                ("body", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "implementation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="implementations.implementation",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="implementation_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "upvotes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="upvoted_implementation_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
