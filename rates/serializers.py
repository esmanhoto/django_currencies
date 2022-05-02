from rest_framework import serializers
from .models import Rate


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('date', 'euro', 'real', 'yen')
