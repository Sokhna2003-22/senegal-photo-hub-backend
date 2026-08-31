from django.db import models
from django.utils.crypto import get_random_string
from apps.accounts.models import User


def generate_access_code():
    return get_random_string(8).upper()


class ClientGallery(models.Model):
    photographer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='galleries'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    access_code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_access_code
    )
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.client_name}"

    class Meta:
        ordering = ['-created_at']


class Photo(models.Model):
    gallery = models.ForeignKey(
        ClientGallery, on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='photos/%Y/%m/')
    title = models.CharField(max_length=200, blank=True)
    is_downloadable = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.gallery.title}"

    class Meta:
        ordering = ['uploaded_at']