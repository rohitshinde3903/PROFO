# Generated by Django 5.1.4 on 2024-12-16 16:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_socialmedialink_click_count_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkClick",
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
                ("clicked_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clicks",
                        to="users.socialmedialink",
                    ),
                ),
            ],
        ),
    ]