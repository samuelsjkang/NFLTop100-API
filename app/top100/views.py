from rest_framework import viewsets, mixins, permissions
from main.models import Player, Team
from top100 import serializers


class BaseAttributeViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    # Base viewset for player attributes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class PlayerViewSet(BaseAttributeViewSet):
    # Manage players in db
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class TeamViewSet(BaseAttributeViewSet):
    # Manage teams in db
    queryset = Team.objects.all()
    serializer_class = serializers.TeamSerializer
