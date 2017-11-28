from pygame.math import Vector2
from pong.constants import *
import pong.entities as entities
import unittest


class BallInstantiationTestCase(unittest.TestCase):

    def test_ball_create(self):
        ball = entities.Ball()
        self.assertIsNotNone(ball)

    def test_ball_create_no_location(self):
        ball = entities.Ball()
        self.assertIsNotNone(ball)
        self.assertEqual(ball.location.x, 0)
        self.assertEqual(ball.location.y, 0)

    def test_ball_instantiate_in_middle_of_field(self):
        """Instantiate the ball in the middle of the field"""
        x = (FIELD_WIDTH - entities.Ball.WIDTH) / 2.0
        y = (FIELD_HEIGHT - entities.Ball.HEIGHT) / 2.0
        ball = entities.Ball(Vector2(x, y))
        self.assertEqual(ball.location.x, x)
        self.assertEqual(ball.location.y, y)


class BallMovementTestCase(unittest.TestCase):

    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world
        self.origin = Vector2(300, 200)
        self.ball = entities.Ball(self.origin)
        self.heading = Vector2(1, 1).normalize()   # Head 45 degrees downwards.
        self.ball.heading = self.heading

    def test_origin(self):
        self.assertEqual(self.ball.get_rect().x, self.origin.x)
        self.assertEqual(self.ball.get_rect().y, self.origin.y)

    def test_update_move(self):
        """Test that the ball will move on one update."""
        old_pos = Vector2(self.ball.location)
        self.ball.update(TICK_SECOND)
        x = self.ball.location.x
        y = self.ball.location.y
        self.assertAlmostEqual(x, old_pos.x + TICK_SECOND * self.heading.x * self.ball.speed)
        self.assertAlmostEqual(y, old_pos.y + TICK_SECOND * self.heading.y * self.ball.speed)


class BallBounceTopWallTestCase(unittest.TestCase):

    def setUp(self):
        # Spawn a ball just below the top wall
        self.ball = entities.Ball(Vector2())
        self.heading = Vector2(1, -1).normalize()   # Move 45 degrees: /_
        self.ball.heading = self.heading

    def test_update(self):
        """The ball's heading should flip on the Y axis; from going up to going down"""
        self.ball.update(TICK_SECOND)
        self.assertEqual(self.ball.heading.y, self.heading.y * -1)
        self.assertEqual(self.ball.location.y, 0)


class BallBounceBottomWallTestCase(unittest.TestCase):

    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world

        # Spawn a ball just above the bottom wall
        self.ball = entities.Ball(Vector2(0, FIELD_HEIGHT - entities.Ball.HEIGHT))
        self.heading = Vector2(1, 1).normalize()   # Move 45 degrees downwards
        self.ball.heading = self.heading

    def test_update(self):
        """The ball's heading should flip on the Y axis; from going up to going down"""
        self.ball.update(TICK_SECOND)
        self.assertEqual(self.ball.heading.y, self.heading.y * -1)
        self.assertEqual(self.ball.location.y, FIELD_HEIGHT - self.ball.HEIGHT)


class BallHitRightPaddleTestCase(unittest.TestCase):

    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world

        px = FIELD_WIDTH - entities.Paddle.WIDTH * 2
        py = 0
        self.right_paddle = entities.Paddle((px, py))

        ball_dir = Vector2(1, 0)  # Going straight right
        self.ball = entities.Ball((px - entities.Ball.WIDTH, py)) # Place it before the paddle
        self.ball.heading = ball_dir

    def test_ball_and_paddle_in_world(self):
        """Test that both ball and the paddle are in the world"""
        self.assertIn(self.ball, self.world)
        self.assertIn(self.right_paddle, self.world)

    def test_ball_bounce_right_paddle(self):
        self.ball.update(TICK_SECOND)
        self.assertLess(self.ball.heading.x, 0)  # The ball is now going to the left

        br = self.ball.get_rect()
        self.assertEqual(br.right, self.right_paddle.get_rect().x)


class BallHitLeftPaddleTestCase(unittest.TestCase):

    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world

        px = entities.Paddle.WIDTH
        py = 0
        self.left_paddle = entities.Paddle((px, py))

        ball_dir = Vector2(-1, 0)  # Going straight left
        self.ball = entities.Ball((px + entities.Paddle.WIDTH, py)) # Place it before the paddle
        self.ball.heading = ball_dir

    def test_ball_bounce_left_paddle(self):
        self.ball.update(TICK_SECOND)
        self.assertGreater(self.ball.heading.x, 0)  # The ball is now going to the right

        br = self.ball.get_rect()
        self.assertEqual(br.left, self.left_paddle.get_rect().right)


class BallIsAliveTestCase(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        entities.Ball.world = self.world

    def test_ball_is_alive_when_in_world_bounds(self):
        ball = entities.Ball((100, 100))
        self.assertTrue(ball.alive())

    def test_ball_is_not_alive_when_out_of_world_bounds(self):
        ball = entities.Ball((-100, 100)) # Negative X
        self.assertFalse(ball.alive())

    def test_ball_not_alive_when_no_world(self):
        """alive method should return false if the ball has no world."""
        entities.Ball.world = None
        ball = entities.Ball((0, 0))
        self.assertFalse(ball.alive())


class BallResetTestCase(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        self.ball = entities.Ball(Vector2(100, 100))  # Place the ball away from the middle of the field
        self.ball.world = self.world
        self.world.add(self.ball)

    def test_ball_reset_to_field_mid(self):
        self.assertIsNotNone(self.ball.world)
        self.ball.reset()
        ball_mid_field_x = (self.world.WIDTH - self.ball.WIDTH) / 2
        ball_mid_field_y = (self.world.HEIGHT - self.ball.HEIGHT) / 2
        self.assertEqual(self.ball.location, Vector2(ball_mid_field_x, ball_mid_field_y))

    def test_speed_reset(self):
        self.ball.speed = 10000
        self.ball.reset()
        self.assertEqual(self.ball.speed, self.ball.SPEED)

    def test_heading_reset(self):
        pass


# class BallResetWithPlayersTestCase(unittest.TestCase):
#     pass