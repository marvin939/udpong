import json
import pygame
# from pong.constants import *
import pong
import pong.constants
from pygame.math import Vector2
# import pong.common as common


class GameEntity(pygame.sprite.Sprite):
    world = None
    HEIGHT = 16
    WIDTH = 16

    def __init__(self, location=None):
        if self.world is None:
            super().__init__()
        else:
            super().__init__(GameEntity.world)    # Place this in the world automatically
        self.location = Vector2(location) if location is not None else Vector2()

    def update(self, seconds_passed):
        pass

    def get_rect(self):
        x, y = self.location
        return pygame.Rect(int(x), int(y), self.WIDTH, self.HEIGHT)

    def get_collision(self):
        """Gets the GameEntity object that this has collided with"""
        if self.world is None:
            return None

        for entity in self.world.sprites():
            if self is entity:
                continue
            if self.get_rect().colliderect(entity.get_rect()):
                return entity
        return None

    def json_string(self):
        attributes = dict()
        attributes['class_name'] = self.__class__.__name__
        attributes['location'] = (*self.location,)
        # attributes.update(self.__dict__)
        # return json.dumps(self, default=common.convert_to_builtin_type, separators=(',',':'))
        return json.dumps(attributes, separators=(',',':'))


class Ball(GameEntity):
    HEIGHT = 16
    WIDTH = 16
    SIZE = (WIDTH, HEIGHT)
    COLOR = pygame.color.Color('white')
    SPEED = 200
    # WORLD = None

    # container = None

    def __init__(self, location=None):
        super().__init__(location=location)
        # GameEntity.__init__(self)
        # pygame.sprite.Sprite.__init__(self, self.world)
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.speed = self.SPEED
        self.heading = Vector2()

    def update(self, seconds_passed):
        self.location += seconds_passed * self.speed * self.heading

        if self.location.y < 0:
            self.location.y = 0
            self.heading = self.heading.reflect(Vector2(0, 1))

        elif self.location.y + self.HEIGHT > pong.constants.FIELD_HEIGHT:
            self.location.y = pong.constants.FIELD_HEIGHT - self.HEIGHT
            self.heading = self.heading.reflect(Vector2(0, 1))

        collision = self.get_collision()
        if collision is not None:
            if self.location.x < collision.location.x:
                # Ball is left of paddle when they collided...
                self.location.x = collision.location.x - self.WIDTH
            else:
                # Ball is right of paddle when they collided...
                self.location.x = collision.location.x + collision.WIDTH
            self.heading.reflect_ip(Vector2(1, 0))  # Flip horizontal movement
        # ball_rect = self.get_rect()

    def alive(self):
        if self.world is None:
            return False
        if not self.get_rect().colliderect(pygame.Rect(0, 0, self.world.WIDTH, self.world.HEIGHT)):
            return False
        return True

    def reset(self):
        if self.world is None:
            return
        # Put the ball in the middle of the field.
        # self.location = Vector2((self.world.WIDTH - self.WIDTH) / 2, (self.world.HEIGHT - self.HEIGHT) / 2)
        self.location = self.default_location()
        self.speed = self.SPEED

    def default_location(self):
        if self.world is None:
            return Vector2()
        return Vector2((self.world.WIDTH - self.WIDTH) / 2, (self.world.HEIGHT - self.HEIGHT) / 2)


class Paddle(GameEntity):
    WIDTH = 16
    HEIGHT = WIDTH * 5
    SIZE = (WIDTH, HEIGHT)
    COLOR = pygame.color.Color('white')
    SPEED = 200

    def __init__(self, location=None):
        super().__init__(location=location)
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.speed = self.SPEED
        self.heading = Vector2()

    def update(self, seconds_passed):
        self.move(seconds_passed)

    def move(self, seconds_passed):
        self.location += self.speed * self.heading * seconds_passed

        if self.world is None:
            return

        # Clamp it's Y location in the field.
        if self.location.y + self.HEIGHT > self.world.HEIGHT:
            self.location.y = self.world.HEIGHT - self.HEIGHT
            self.heading = Vector2()

        elif self.location.y < 0:
            self.location.y = 0
            self.heading = Vector2()


class World(pygame.sprite.Group):
    WIDTH = pong.constants.FIELD_WIDTH
    HEIGHT = pong.constants.FIELD_HEIGHT
    COLOR = pygame.color.Color('black')
    X = 0
    Y = 0

    def __init__(self):
        pygame.sprite.Group.__init__(self)