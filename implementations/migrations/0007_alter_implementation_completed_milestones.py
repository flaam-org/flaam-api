# Generated by Django 3.2.7 on 2021-10-02 15:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("implementations", "0006_auto_20211002_2105"),
    ]

    operations = [
        migrations.AlterField(
            model_name="implementation",
            name="completed_milestones",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(),
                blank=True,
                default=list,
                size=10,
            ),
        ),
    ]