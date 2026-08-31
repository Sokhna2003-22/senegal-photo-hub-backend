from rest_framework import serializers
from .models import PortfolioAlbum, PortfolioPhoto
from apps.accounts.serializers import UserSerializer


class PortfolioPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioPhoto
        fields = ['id', 'image_url', 'caption']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class PortfolioAlbumSerializer(serializers.ModelSerializer):
    photos = PortfolioPhotoSerializer(many=True, read_only=True)
    photographer = UserSerializer(read_only=True)
    cover_url = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioAlbum
        fields = ['id', 'title', 'description', 'category',
                  'cover_url', 'is_public', 'created_at',
                  'photographer', 'photos', 'photo_count']

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_photo_count(self, obj):
        return obj.photos.count()