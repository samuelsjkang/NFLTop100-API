from rest_framework import serializers
from main.models import Player, Team, Position


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Team.objects.all()
    )
    position = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Position.objects.all()
    )

    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'ranking',
            'team',
            'position',
            'last_ranking',
            'youtube_link'
        )
        read_only_fields = ('id',)


class DetailSerializer(PlayerSerializer):
    team = TeamSerializer(many=True, read_only=True)
    position = PositionSerializer(many=True, read_only=True)
