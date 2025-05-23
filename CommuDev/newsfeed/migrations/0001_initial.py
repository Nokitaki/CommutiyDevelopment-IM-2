# Generated by Django 5.1.1 on 2024-11-04 07:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewsFeed",
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
                ("created_by", models.CharField(default="Anonymous", max_length=255)),
                ("post_description", models.TextField(default="create a post")),
                ("post_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("post_type", models.CharField(default="Active", max_length=20)),
                ("like_count", models.IntegerField(default=0)),
            ],
        ),
    ]
