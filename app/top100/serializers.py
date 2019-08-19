from rest_framework import serializers
from main.models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'ranking', 'last_ranking')
        read_only_fields = ('id',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
        read_only_fields = ('id',)
