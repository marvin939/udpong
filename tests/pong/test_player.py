# import pong.entities as entities
import unittest
import pong.game as game
import pong.entities as entities
from pong.constants import *
from pygame.math import Vector2


class PlayerInstantiationTestCase(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world

    def test_instantiation_player_1_score(self):
        player1 = game.Player(PLAYER1)
        self.assertEqual(player1.score, 0)

    def test_instantiation_player_1_location(self):
        """Player 1 should spawn on the left side of the field"""
        player1 = game.Player(PLAYER1)

        # expected coordinates
        expx = PLAYER_MARGIN
        expy = (self.world.HEIGHT - player1.HEIGHT) / 2
        self.assertEqual(player1.location, Vector2(expx, expy))

    def test_instantiation_player_2_location(self):
        """Player 2 should spawn on the right side of the field"""
        player2 = game.Player(PLAYER2)
        expx = self.world.WIDTH - PLAYER_MARGIN - player2.WIDTH
        expy = (self.world.HEIGHT - player2.HEIGHT) / 2
        self.assertEqual(player2.location, Vector2(expx, expy))
