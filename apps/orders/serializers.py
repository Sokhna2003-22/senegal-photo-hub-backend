from rest_framework import serializers
from .models import Order
from apps.accounts.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    photographer = UserSerializer(read_only=True)
    photographer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'photographer', 'photographer_id',
                  'service_type', 'event_date', 'location',
                  'message', 'status', 'price', 'created_at']

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)