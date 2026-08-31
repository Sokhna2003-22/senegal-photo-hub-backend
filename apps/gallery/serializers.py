from rest_framework import serializers
from .models import ClientGallery, Photo


class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'title', 'is_downloadable', 'uploaded_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ClientGallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    photo_count = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientGallery
        fields = ['id', 'title', 'description', 'client_name',
                  'client_email', 'access_code', 'cover_url',
                  'is_active', 'created_at', 'photo_count', 'photos']

    def get_photo_count(self, obj):
        return obj.photos.count()

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None