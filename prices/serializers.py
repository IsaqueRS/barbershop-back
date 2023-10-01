from rest_framework import serializers
from .models import Prices


class PricesSerializers(serializers.Serializer):
    class Meta:
        model = Prices
        fields = '__all__'
        depth = 1