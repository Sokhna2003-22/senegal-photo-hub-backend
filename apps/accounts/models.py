from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('photographer', 'Photographe'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_photographer(self):
        return self.role == 'photographer'

    def is_client(self):
        return self.role == 'client'

    def __str__(self):
        return f"{self.username} ({self.role})"


class PhotographerProfile(models.Model):
    PLAN_CHOICES = (
        ('free', 'Gratuit'),
        ('basic', 'Basic - 1000 FCFA/mois'),
        ('premium', 'Premium - 3000 FCFA/mois'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='photographer_profile')
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"