from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, MaxLengthValidator
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

class Breach(models.Model):
    """
    Модель, представляющая утечку данных.
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('processed', 'Processed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='breaches'
    )
    service_name = models.CharField(max_length=255)
    breach_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        user_email = self.user.email if self.user else "Unknown User"
        return f"{self.service_name} - {self.breach_date} - {user_email}"

    class Meta:
        verbose_name = "Data Breach"
        verbose_name_plural = "Data Breaches"
        ordering = ['-breach_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['service_name']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        if not self.service_name:
            raise ValidationError("Service name is required.")
        if not self.breach_date:
            raise ValidationError("Breach date is required.")
        if not self.status:
            raise ValidationError("Status is required.")
        if self.location and len(self.location) > 255:
            raise ValidationError("Location exceeds maximum length of 255 characters.")
        if self.data_type and len(self.data_type) > 255:
            raise ValidationError("Data type exceeds maximum length of 255 characters.")
        if self.source and len(self.source) > 255:
            raise ValidationError("Source exceeds maximum length of 255 characters.")
        if self.description and len(self.description) > 1000:
            raise ValidationError("Description exceeds maximum length of 1000 characters.")

class Feedback(models.Model):
    """
    Модель, представляющая обратную связь от пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField(
        validators=[MaxLengthValidator(5000)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'} - {self.created_at}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

class Report(models.Model):
    """
    Модель, представляющая сгенерированный отчет.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.JSONField(default=dict)
    report_type = models.CharField(
        max_length=10,
        choices=[('pdf', 'PDF'), ('html', 'HTML')],
        default='pdf'
    )
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        user_email = self.user.email if self.user else "Unknown User"
        return f"Report for {user_email} - {self.generated_at}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['generated_at']),
        ]

    def clean(self):
        if self.email:
            try:
                validate_email(self.email)
            except ValidationError:
                raise ValidationError("Invalid email address.")

class SupportTicket(models.Model):
    """
    Модель, представляющая тикет поддержки.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(
        max_length=255,
        validators=[MaxLengthValidator(255)]
    )
    description = models.TextField(
        validators=[MaxLengthValidator(5000)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket: {self.title} - {self.get_status_display()}"

    def get_status_display(self):
        """Возвращает человеко-читаемый статус тикета."""
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')

    class Meta:
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

class UserProfile(models.Model):
    """
    Модель, представляющая профиль пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    telegram_id = models.CharField(max_length=255, blank=True, null=True)
    notification_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [
            models.Index(fields=['user']),
        ]

    def clean(self):
        if self.bio and len(self.bio) > 500:
            raise ValidationError("Bio exceeds maximum length of 500 characters.")
        if self.location and len(self.location) > 255:
            raise ValidationError("Location exceeds maximum length of 255 characters.")
        if self.telegram_id and len(self.telegram_id) > 255:
            raise ValidationError("Telegram ID exceeds maximum length of 255 characters.")

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            UserProfile.objects.create(user=instance)
        else:
            UserProfile.objects.get_or_create(user=instance)
    except Exception as e:
        # Логирование ошибки
        logger.error(f"Error creating or updating user profile: {e}")
