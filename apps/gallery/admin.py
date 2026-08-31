from django.contrib import admin
from .models import ClientGallery, Photo


@admin.register(ClientGallery)
class ClientGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'photographer', 'client_name', 'access_code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'client_name', 'access_code']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'is_downloadable', 'uploaded_at']