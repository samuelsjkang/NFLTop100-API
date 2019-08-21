from rest_framework import viewsets, mixins, permissions
from main.models import Player, Team, Position
from top100 import serializers


class BaseAttributeViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    # Base viewset for player attributes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(player__isnull=False)
        return queryset.order_by('id').distinct()

    def perform_create(self, serializer):
        serializer.save()


class PlayerViewSet(viewsets.ModelViewSet):
    # Manage players in db
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        team = self.request.query_params.get('team')
        position = self.request.query_params.get('position')
        queryset = self.queryset
        if team:
            team_ids = self.params_to_ints(team)
            queryset = queryset.filter(team__id__in=team_ids)
        if position:
            position_ids = self.params_to_ints(position)
            queryset = queryset.filter(position__id__in=position_ids)
        return queryset.order_by('id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save()


class TeamViewSet(BaseAttributeViewSet):
    # Manage teams in db
    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer


class PositionViewSet(BaseAttributeViewSet):
    # Manage positions in db
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer
