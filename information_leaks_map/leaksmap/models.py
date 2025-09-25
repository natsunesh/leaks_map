"""
Models for the LeaksMap application.
This module contains all the database models used by the application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Breach(models.Model):
    """
    Model representing a data breach.
    """
    service_name = models.CharField(max_length=255)
    breach_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.service_name} - {self.breach_date} - {self.email}"

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['service_name']),
        ]

class Feedback(models.Model):
    """
    Model representing user feedback.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'} - {self.created_at}"

class Report(models.Model):
    """
    Model representing a generated report.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.JSONField(default=dict)

    def __str__(self):
        return f"Report for {self.email} - {self.generated_at}"

class SupportTicket(models.Model):
    """
    Model representing a support ticket.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket: {self.title} - {self.get_status_display()}"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')

class UserProfile(models.Model):
    """
    Model representing a user profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
