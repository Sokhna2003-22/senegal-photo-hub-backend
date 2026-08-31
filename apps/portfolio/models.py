from django.db import models
from apps.accounts.models import User


class PortfolioAlbum(models.Model):
    CATEGORY_CHOICES = (
        ('mariage', 'Mariage'),
        ('portrait', 'Portrait'),
        ('evenement', 'Événement'),
        ('mode', 'Mode'),
        ('nature', 'Nature'),
        ('autre', 'Autre'),
    )

    photographer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='albums'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='autre')
    cover_image = models.ImageField(upload_to='portfolio/covers/')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} par {self.photographer.username}"

    class Meta:
        ordering = ['-created_at']


class PortfolioPhoto(models.Model):
    album = models.ForeignKey(
        PortfolioAlbum, on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='portfolio/photos/%Y/%m/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de l'album {self.album.title}"