from django.contrib import admin
from .models import PortfolioAlbum, PortfolioPhoto


@admin.register(PortfolioAlbum)
class PortfolioAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'photographer', 'category', 'is_public', 'created_at']
    list_filter = ['category', 'is_public']
    search_fields = ['title', 'photographer__username']


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display = ['album', 'uploaded_at']