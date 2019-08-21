from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Position, Player
from top100.serializers import PositionSerializer

UserModel = get_user_model()
POSITIONS_URL = reverse('top100:position-list')


class PositionsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that request is successful
    def test_get_positions(self):
        Position.objects.create(name='DT')
        Position.objects.create(name='QB')

        res = self.client.get(POSITIONS_URL)
        positions = Position.objects.all().order_by('name')
        serializer = PositionSerializer(positions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminPositionsAPITests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            'test@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests position creation
    def test_position_creation(self):
        payload = {'name': 'Test Position'}
        self.client.post(POSITIONS_URL, payload)
        position_exists = Position.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(position_exists)

    # Tests invalid position creation
    def test_invalid_position(self):
        payload = {'name': ''}
        res = self.client.post(POSITIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests filtering positions that have players in the top 100
    def test_filter_assigned_positions(self):
        position = Position.objects.create(name='LB')
        Position.objects.create(name='WR')
        player1 = Player.objects.create(
            name='Von Miller',
            ranking=10,
            last_ranking=9
        )
        player1.position.add(position)
        player2 = Player.objects.create(
            name='Luke Kuechly',
            ranking=24,
            last_ranking=12
        )
        player2.position.add(position)
        res = self.client.get(POSITIONS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
