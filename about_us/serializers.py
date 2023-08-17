from rest_framework import serializers
from .models import AbousUs, TermsOfUse


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbousUs
        fields = '__all__'


class TermsOfUseSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsOfUse
        fields = '__all__'
