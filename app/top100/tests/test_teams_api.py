from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Team, Player
from top100.serializers import TeamSerializer

UserModel = get_user_model()
TEAMS_URL = reverse('top100:team-list')


class TeamsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that request is successful
    def test_get_teams(self):
        Team.objects.create(name='Los Angeles Rams')
        Team.objects.create(name='New Orleans Saints')

        res = self.client.get(TEAMS_URL)
        teams = Team.objects.all().order_by('name')
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminTeamsAPITests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            'test@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests team creation
    def test_team_creation(self):
        payload = {'name': 'Test Team'}
        self.client.post(TEAMS_URL, payload)
        team_exists = Team.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(team_exists)

    # Tests invalid team creation
    def test_invalid_team(self):
        payload = {'name': ''}
        res = self.client.post(TEAMS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests filtering teams that have players in the top 100
    def test_filter_assigned_teams(self):
        team = Team.objects.create(name='Chicago Bears')
        Team.objects.create(name='Dalls Cowboys')
        player1 = Player.objects.create(
            name='Khalil Mack',
            ranking=3,
            last_ranking=16
        )
        player1.team.add(team)
        player2 = Player.objects.create(
            name='Akiem Hicks',
            ranking=39,
            last_ranking=00
        )
        player2.team.add(team)
        res = self.client.get(TEAMS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
