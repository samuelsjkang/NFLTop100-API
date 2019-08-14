from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Player
from top100.serializers import PlayerSerializer

UserModel = get_user_model()
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


class AdminPlayersAPITests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            'test@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests player creation
    def test_player_creation(self):
        payload = {'name': 'Test Player'}
        self.client.post(PLAYERS_URL, payload)
        player_exists = Player.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(player_exists)

    # Tests invalid player creation
    def test_invalid_player(self):
        payload = {'name': ''}
        res = self.client.post(PLAYERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
