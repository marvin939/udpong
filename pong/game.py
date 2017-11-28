import pong.constants as consts
from pygame.math import Vector2
import pong.entities as entities


class Player(entities.Paddle):

    def __init__(self, player_num):
        super().__init__(None)
        self.score = 0
        self.number = player_num
        self.reset_location()

    def reset_location(self):
        if self.world is None:
            return
        new_y = (self.world.HEIGHT - self.HEIGHT) / 2
        new_x = -1
        if self.number in (consts.PLAYER1, consts.PLAYER_LEFT):
            new_x = consts.PLAYER_MARGIN    # Left side
        elif self.number in (consts.PLAYER2, consts.PLAYER_RIGHT):
            new_x = self.world.WIDTH - consts.PLAYER_MARGIN - self.WIDTH    # Right side
        self.location = Vector2(new_x, new_y)

    def __repr__(self):
        return 'Player{this.number} :: score={this.score}; location={this.location}'.format(this=self)


class Pong(entities.World):

    def __init__(self):
        super().__init__()
        entities.GameEntity.world = self

        self.player1 = Player(consts.PLAYER1)
        self.player2 = Player(consts.PLAYER2)
        self.ball = entities.Ball()

        self.player1.world = self
        self.player2.world = self
        self.ball.world = self

        self.player1.reset_location()
        self.player2.reset_location()
        self.ball.reset()
        self.add(self.player1, self.player2, self.ball)

    def ball_side(self):
        """Return the player the ball is nearest to"""
        ball_center = Vector2(self.ball.get_rect().center)
        if ball_center.x < self.WIDTH / 2:
            return self.player1
        else:
            return self.player2

    def handle_scores(self):
        """Responsible for incrementing scores, and resetting the ball's position when it dies"""
        if not self.ball.alive():
            # increment scores first
            if self.ball_side() is self.player1:
                self.player2.score += 1
            else:
                self.player1.score += 1
            self.ball.reset()

    def update(self, seconds_passed):
        super().update(seconds_passed)
        self.handle_scores()
