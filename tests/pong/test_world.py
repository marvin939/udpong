from pygame.math import Vector2
import unittest
import pong.entities as entities


class WorldTestCase(unittest.TestCase):
    pass


class AutoAddToWorldTestCase(unittest.TestCase):
    """Entities get automatically added to a world object if the
    world variable from entities.GameEntity is overwritten"""

    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world
        entities.Ball.world = self.world

    def test_ball_automatically_added_to_world(self):
        ball = entities.Ball()
        self.assertIn(ball, self.world)

    def test_paddle_automatically_added_to_world(self):
        paddle = entities.Paddle()
        self.assertIn(paddle, self.world)