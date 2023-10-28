from rest_framework import serializers
from .models import NFLPlayer

class NFLPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLPlayer
        fields = '__all__'
        