# Generated by Django 5.1.2 on 2024-12-17 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_socialmedialink_options_customuser_following_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialmedialink",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="Optional description about the social media link",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="socialmedialink",
            name="is_active",
            field=models.BooleanField(
                default=True, help_text="Uncheck this to disable the social media link."
            ),
        ),
    ]
