# Generated by Django 3.2.7 on 2021-09-30 06:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ideas", "0004_auto_20210913_1858"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ideas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
