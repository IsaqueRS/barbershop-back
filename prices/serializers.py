from rest_framework import serializers
from .models import Prices


class PricesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'
