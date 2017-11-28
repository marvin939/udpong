import pong.entities as entities
from pong.constants import *
import unittest
import pygame
from pygame.math import Vector2


class PaddleInstantiationTestCase(unittest.TestCase):

    def test_paddle_create_no_location(self):
        paddle = entities.Paddle()
        self.assertEqual(paddle.location.x, 0)
        self.assertEqual(paddle.location.y, 0)

    def test_paddle_instantiate_in_middle_of_field(self):
        """Instantiate the ball in the middle of the field"""
        x = (FIELD_WIDTH - entities.Paddle.WIDTH) / 2.0
        y = (FIELD_HEIGHT - entities.Paddle.HEIGHT) / 2.0
        paddle = entities.Paddle(Vector2(x, y))
        self.assertEqual(paddle.location.x, x)
        self.assertEqual(paddle.location.y, y)


class PaddleTestCase(unittest.TestCase):
    def setUp(self):
        self.px = 100
        self.py = 50
        self.paddle = entities.Paddle(location=Vector2(self.px, self.py))

    @unittest.skip
    def test_rect_property(self):
        """Test it's rect() property which returns a new rectangle based on its current location, its HEIGHT and WIDTH"""
        r = self.paddle.rect
        self.assertTrue(isinstance(r, pygame.Rect))


class PaddleMoveTestCase(unittest.TestCase):

    def setUp(self):
        entities.GameEntity.world = entities.World()
        self.paddle_pos = Vector2(100, 50)
        self.paddle = entities.Paddle(self.paddle_pos)

    def test_move_heading_down(self):
        heading = Vector2(0, 1)
        self.paddle.heading = heading
        self.assertEqual(self.paddle.heading, heading)

        self.paddle.update(TICK_SECOND)
        expected_pos = self.paddle_pos + self.paddle.speed * heading * TICK_SECOND

        self.assertNotEqual(self.paddle.location.y, self.paddle_pos.y)
        self.assertEqual(self.paddle.location.x, self.paddle_pos.x)
        self.assertEqual(self.paddle.location, expected_pos)


class PaddleMoveBeyondBottomWallTestCase(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world
        self.paddle = entities.Paddle(Vector2(0, FIELD_HEIGHT - entities.Paddle.HEIGHT))
        self.heading = Vector2(0, 1)    # Going downwards
        self.paddle.heading = self.heading

    def test_correct_position_when_moving_beyond_bottom_wall(self):
        """The idea is to reset the paddle's heading/direction to Vector 0, and correct the paddle's y location"""
        self.paddle.update(TICK_SECOND)
        self.assertEqual(self.paddle.location.y, FIELD_HEIGHT - self.paddle.HEIGHT)

    def test_heading_reset(self):
        self.paddle.update(TICK_SECOND)
        self.assertEqual(self.paddle.heading.x, 0)
        self.assertEqual(self.paddle.heading.y, 0)


class PaddleMoveBeyondTopWallTestCase(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world
        self.paddle = entities.Paddle(Vector2(0, 0))
        self.heading = Vector2(0, -1)    # Going upwards
        self.paddle.heading = self.heading

    def test_correct_position_when_moving_beyond_bottom_wall(self):
        """The idea is to reset the paddle's heading/direction to Vector 0, and correct the paddle's y location"""
        self.paddle.update(TICK_SECOND)
        self.assertEqual(self.paddle.location.y, 0)

    def test_heading_reset(self):
        self.paddle.update(TICK_SECOND)
        self.assertEqual(self.paddle.heading.x, 0)
        self.assertEqual(self.paddle.heading.y, 0)


