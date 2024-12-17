from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_email_verified = models.BooleanField(default=False)

    bio = models.TextField(blank=True, null=True)  # Optional bio field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional profile picture
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follow',
        through_fields=('follower', 'followed'),
        related_name='followers',  # Users who follow this user
    )


from django.db import models

class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following_relationships',  # Unique reverse accessor
    )
    followed = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower_relationships',  # Unique reverse accessor
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Prevent duplicates


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)



from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings
from django.utils import timezone


class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Instagram', 'Instagram'),
        ('LinkedIn', 'LinkedIn'),
        ('YouTube', 'YouTube'),
        ('GitHub', 'GitHub'),
        ('Website', 'Personal Website'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='social_links',
        on_delete=models.CASCADE
    )
    platform = models.CharField(
        max_length=100,
        choices=PLATFORM_CHOICES,
        default='Other'
    )
    url = models.URLField(help_text="Enter the full URL (e.g., https://example.com)")
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional description about the social media link"
    )
    click_count = models.PositiveIntegerField(default=0, editable=False)  # Track the number of clicks
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update the timestamp when modified
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck this to disable the social media link."
    )

    class Meta:
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
        ordering = ['-created_at']  # Default ordering: newest first

    def increment_click_count(self):
        """Increments the click count by 1."""
        self.click_count += 1
        self.save()

    def __str__(self):
        return f"{self.platform} - {self.user.username}"



from django.db import models
from django.utils import timezone

class LinkClick(models.Model):
    link = models.ForeignKey(SocialMediaLink, related_name="clicks", on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(default=timezone.now)



    def save(self, *args, **kwargs):
        # Ensure clicks are logged once per day for each link
        if not self.pk:
            self.clicked_at = timezone.localtime(self.clicked_at).date()  # Only store the date part
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.link.platform} clicked on {self.clicked_at}"