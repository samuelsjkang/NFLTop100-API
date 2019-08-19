from django.test import TestCase
from main import models


class PlayerModelTests(TestCase):
    # Test to check player's name
    def test_player_str(self):
        player = models.Player.objects.create(
            name='Aaron Donald',
            ranking=1,
            last_ranking=7
        )
        self.assertEqual(str(player), player.name)

    # Test to check team name
    def test_team_str(self):
        team = models.Team.objects.create(
            name='Los Angeles Rams'
        )
        self.assertEqual(str(team), team.name)
