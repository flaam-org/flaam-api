# Generated by Django 3.2.7 on 2021-09-05 10:50

from django.db import migrations, models

import accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Username must be 4 to 15 characters long.\nIt may only contain lowercase alphabets, numbers and underscores.\nIt shouldn't start or end with underscores.\nIt shouldn't contain consecutive underscores",
                max_length=32,
                unique=True,
                validators=[accounts.validators.UsernameValidator],
                verbose_name="username",
            ),
        ),
    ]