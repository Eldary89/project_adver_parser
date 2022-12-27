from rest_framework.serializers import ModelSerializer

from .models import Advertisement


class AdvertisementModelSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
