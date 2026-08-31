from rest_framework import serializers
from .models import User, PhotographerProfile


class PhotographerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotographerProfile
        fields = ['bio', 'city', 'website', 'instagram', 'plan']


class UserSerializer(serializers.ModelSerializer):
    photographer_profile = PhotographerProfileSerializer(read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'role', 'avatar_url', 'photographer_profile']

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'role', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == 'photographer':
            PhotographerProfile.objects.create(user=user)

        return user