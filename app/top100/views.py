from rest_framework import viewsets, mixins, permissions
from main.models import Player, Team, Position
from top100 import serializers


class BaseAttributeViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    # Base viewset for player attributes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class PlayerViewSet(viewsets.ModelViewSet):
    # Manage players in db
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
