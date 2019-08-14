from django.test import TestCase
from main import models


class PlayerModelTests(TestCase):
    # Test to check player's team
    def test_player_str(self):
        player = models.Player.objects.create(
            name='Aaron Donald'
        )
        self.assertEqual(str(player), player.name)
