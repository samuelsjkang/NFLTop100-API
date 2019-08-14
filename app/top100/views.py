from rest_framework import viewsets, mixins, permissions
from main.models import Player
from top100 import serializers


class PlayerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    # Manage players in db
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
