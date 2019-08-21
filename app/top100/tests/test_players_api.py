from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Player, Team, Position
from top100.serializers import PlayerSerializer, DetailSerializer

UserModel = get_user_model()
PLAYERS_URL = reverse('top100:player-list')


# Creates a sample player
def sample_player(**params):
    defaults = {
        'name': 'Sample Player',
        'ranking': 4,
        'last_ranking': 7
    }
    defaults.update(params)
    return Player.objects.create(**defaults)


# Creates a sample team
def sample_team(name='Seattle Seahawks'):
    return Team.objects.create(name=name)


# Creates a sample position
def sample_position(name='QB'):
    return Position.objects.create(name=name)


# Return url to player's details
def detail_url(player_id):
    return reverse('top100:player-detail', args=[player_id])


class PlayersAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that request is successful
    def test_get_players(self):
        sample_player()
        sample_player()

        res = self.client.get(PLAYERS_URL)
        players = Player.objects.all().order_by('ranking')
        serializer = PlayerSerializer(players, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Tests viewing player's details
    def test_view_details(self):
        player = sample_player()
        player.team.add(sample_team())
        player.position.add(sample_position())

        url = detail_url(player.id)
        res = self.client.get(url)
        serializer = DetailSerializer(player)
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
        payload = {
            'name': 'Test Player',
            'ranking': 100,
            'last_ranking': 99
        }
        res = self.client.post(PLAYERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        player = Player.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(player, key))

    # Tests player creation w/ team
    def test_player_team(self):
        team = sample_team(name='New England Patriots')
        payload = {
            'name': 'Test Player',
            'ranking': 100,
            'team': team.name,
            'last_ranking': 99
        }
        res = self.client.post(PLAYERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # Tests player creation w/ position
    def test_player_position(self):
        position = sample_position(name='QB')
        payload = {
            'name': 'A Player',
            'ranking': 100,
            'position': position.name,
            'last_ranking': 99
        }
        res = self.client.post(PLAYERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # Tests updating player w/ patch
    def test_patch_player(self):
        player = sample_player()
        player.team.add(sample_team(name='Miami Dolphins'))
        new_team = sample_team(name='Arizona Cardinals')
        payload = {
            'name': 'Updated Player',
            'team': new_team.name
        }
        url = detail_url(player.id)
        res = self.client.patch(url, payload)
        player.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        team = player.team.all()
        self.assertIn(new_team, team)

    # Tests updating player w/ put
    def test_put_player(self):
        player = sample_player()
        player.position.add(sample_position(name='LB'))
        payload = {
            'name': 'Fully-updated Player',
            'ranking': 75,
            'last_ranking': 80
        }
        url = detail_url(player.id)
        res = self.client.put(url, payload)
        player.refresh_from_db()
        self.assertEqual(player.name, payload['name'])
        self.assertEqual(player.ranking, payload['ranking'])
        self.assertEqual(player.last_ranking, payload['last_ranking'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        position = player.position.all()
        self.assertEqual(len(position), 0)


class FilterAPITests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            'test@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests filtering by team
    def test_team_filter(self):
        player1 = sample_player(name='Baker Mayfield')
        player2 = sample_player(name='Antonio Brown')
        team1 = sample_team(name='Cleveland Browns')
        team2 = sample_team(name='Pittsburgh Steelers')
        player1.team.add(team1)
        player2.team.add(team2)
        player3 = sample_player(name='Tom Brady')
        res = self.client.get(
            PLAYERS_URL,
            {'team': f'{team1.id},{team2.id}'}
        )
        serializer1 = PlayerSerializer(player1)
        serializer2 = PlayerSerializer(player2)
        serializer3 = PlayerSerializer(player3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    # Tests filtering by position
    def test_position_filter(self):
        player1 = sample_player(name='Tom Brady')
        player2 = sample_player(name='Julio Jones')
        position1 = sample_position(name='QB')
        position2 = sample_position(name='WR')
        player1.position.add(position1)
        player2.position.add(position2)
        player3 = sample_player(name='Todd Gurley')
        res = self.client.get(
            PLAYERS_URL,
            {'position': f'{position1.id},{position2.id}'}
        )
        serializer1 = PlayerSerializer(player1)
        serializer2 = PlayerSerializer(player2)
        serializer3 = PlayerSerializer(player3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
