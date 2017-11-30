import json
import unittest

from pygame.math import Vector2

import pong
import pong.common as common
import pong.constants as consts
import pong.entities as entities
import pong.game as game


class PongInstantiationTestCase(unittest.TestCase):

    def test_players_and_ball_properties(self):
        pong = game.Pong()
        self.assertIsNotNone(pong.player1)
        self.assertIsNotNone(pong.player2)
        self.assertIsNotNone(pong.ball)

    def test_instantiate(self):
        """Instantiating a Pong object automatically adds 3 entities:
        Player 1 paddle
        Player 2 paddle
        Ball"""
        pong = game.Pong()

        p1 = None
        p2 = None
        b = None
        for e in pong.sprites():
            if isinstance(e, game.Player):
                if e.number == consts.PLAYER1:
                    p1 = e
                elif e.number == consts.PLAYER2:
                    p2 = e
                else:
                    ValueError('Unexpected player number')
            elif isinstance(e, entities.Ball):
                b = e
            else:
                raise ValueError('Unexpected entity: {}'.format(e))
        self.assertIsNotNone(p1)
        self.assertIsNotNone(p2)
        self.assertIsNotNone(b)


class PongHandleScoringTestCase(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()

    def test_handle_score_ball_alive(self):
        """When the ball is still alive, both players should still have 0 score"""
        self.pong.update(consts.TICK_SECOND)
        self.pong.handle_scores()

        self.assertTrue(self.pong.ball.alive())
        self.assertEqual(self.pong.player1.score, 0)
        self.assertEqual(self.pong.player2.score, 0)

    def test_ball_died_reset_to_middle(self):
        """Reset the ball to the middle when it has died."""
        self.pong.ball.location.x = -20  # Put it behind player 1
        self.pong.handle_scores()   # Should reset the ball's position
        self.assertEqual(self.pong.ball.location, self.pong.ball.default_location())

    def test_handle_score_ball_dead_on_player1_side(self):
        """The ball died on player1's side, so increment player 2's score and reset the ball."""
        # Set up
        old_p2_score = self.pong.player2.score
        self.pong.ball.location.x = -entities.Ball.WIDTH
        self.assertFalse(self.pong.ball.alive())
        self.pong.handle_scores()

        self.assertGreater(self.pong.player2.score, old_p2_score)
        self.assertEqual(self.pong.player1.score, 0)    # Make sure player 1's score didn't increase

    def test_handle_score_ball_dead_on_player2_side(self):
        """The ball died on player2's side, so increment player 1's score and reset the ball."""
        old_p1_score = self.pong.player2.score
        self.pong.ball.location.x = self.pong.WIDTH + self.pong.ball.WIDTH
        self.pong.handle_scores()

        self.assertGreater(self.pong.player1.score, old_p1_score)
        self.assertEqual(self.pong.player2.score, 0)    # Make sure player 2's score didn't increase


class PongGetBallSideTestCase(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()

    def test_ball_near_player1(self):
        # Setup: Place ball near player 1
        p1_loc = Vector2(self.pong.player1.location)
        self.pong.ball.location = Vector2(p1_loc.x + 20, p1_loc.y)

        side = self.pong.ball_side()    # ball side returns the player reference the ball is near to.
        self.assertEqual(side, self.pong.player1)

    def test_ball_near_player2(self):
        p2_loc = Vector2(self.pong.player2.location)
        self.pong.ball.location = Vector2(p2_loc.x - 20, p2_loc.y)
        side = self.pong.ball_side()
        self.assertEqual(side, self.pong.player2)


class PongJSONTestCase(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()

    def test_json_pong(self):
        j = self.pong.locations_json()

        decoded = json.loads(j, object_hook=common.from_json)
        self.assertIsInstance(decoded, game.Pong)


class PongUpdateUsingOtherPong(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()
        self.pong.player1.location.y = 100
        self.pong.player2.location.y = 100
        self.pong.ball.location.y = 100

        self.other_pong = game.Pong()

    def test_update(self):
        j = self.pong.locations_json()
        # p = json.loads(j, object_hook=pong.common.from_json)
        self.other_pong.update_with_json(j)
        self.assertEqual(self.other_pong.player1.location, self.pong.player1.location)
        self.assertEqual(self.other_pong.player2.location, self.pong.player2.location)
        self.assertEqual(self.other_pong.ball.location, self.pong.ball.location)
