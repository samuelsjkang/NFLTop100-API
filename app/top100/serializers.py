from rest_framework import serializers
from main.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')
        read_only_fields = ('id',)
