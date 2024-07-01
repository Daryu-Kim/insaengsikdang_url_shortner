from rest_framework import serializers
from .models import ShortUrl

class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = ['id', 'short_url', 'original_url']
