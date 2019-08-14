from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Player
from top100.serializers import PlayerSerializer

PLAYERS_URL = reverse('top100:player-list')


class PlayersAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that request is successful
    def test_get_players(self):
        Player.objects.create(name='Aaron Donald')
        Player.objects.create(name='Drew Brees')

        res = self.client.get(PLAYERS_URL)
        players = Player.objects.all().order_by('name')
        serializer = PlayerSerializer(players, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
