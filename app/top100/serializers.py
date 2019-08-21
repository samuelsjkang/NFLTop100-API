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
    team = serializers.SlugRelatedField(
        many=True,
        queryset=Team.objects.all(),
        slug_field='name'
     )
    position = serializers.SlugRelatedField(
        many=True,
        queryset=Position.objects.all(),
        slug_field='name'
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
