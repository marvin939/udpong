from pygame.math import Vector2
import json
import copy
import pygame.math
import pong


BUFFER_SIZE = 4096


def to_json(obj):
    """Converts an object into a JSON-serializable type.
    Original idea: http://www.diveintopython3.net/serializing.html"""
    obj_class = type(obj).__name__

    if isinstance(obj, pong.common.ClientCommand):
        return {'__class__': obj_class,
                '__value__': obj.__dict__}

    if isinstance(obj, (pygame.math.Vector2, pygame.Rect)):
        return {'__class__': obj_class,
                '__value__': [*obj,]}   # Convert it into a list

    if isinstance(obj, pong.game.Player):
        return {'__class__': obj_class,
                'number': obj.number,
                'score': obj.score,
                'rect': obj.get_rect()}

    if isinstance(obj, pong.entities.GameEntity):
        return {'__class__': obj_class,
                '__value__': obj.get_rect()}

    if isinstance(obj, pong.game.Pong):
        return {'__class__': obj_class,
                'player1': obj.player1,
                'player2': obj.player2,
                'ball': obj.ball,
                'state': None}

    # future: Add game state; eg. WinnerP1, WinnerP2, Idle (ball hasn't launched), Playing
    raise TypeError(repr(obj) + ' is not JSON serializable!')


def from_json(json_obj):
    """Converts a JSON string into a proper object.
    Original idea: customserializer.py from http://www.diveintopython3.net/serializing.html"""
    if '__class__' in json_obj:
        _class = json_obj['__class__']

        if _class == 'ClientCommand':
            return pong.common.ClientCommand(from_dict=json_obj['__value__'])

        if _class == 'Vector2':
            return pygame.math.Vector2(json_obj['__value__'])  # unpack __value__ and turn it into Vector2

        if _class == 'Rect':
            return pygame.Rect(json_obj['__value__'])

        if _class == 'Ball':
            x, y, w, h = (*json_obj['__value__'],)
            ball = pong.entities.Ball((x, y))
            ball.WIDTH, ball.HEIGHT = w, h
            return ball

        if _class == 'Player':
            x, y, w, h = (*json_obj['rect'],)
            player = pong.game.Player(json_obj['number'])
            player.location = pygame.math.Vector2(x, y)
            player.WIDTH, player.HEIGHT = w, h
            player.score = json_obj['score']
            return player

        if _class == 'Pong':
            pong_world = pong.game.Pong()
            pong_world.player1 = json_obj['player1']
            pong_world.player2 = json_obj['player2']
            pong_world.ball = json_obj['ball']
            pong_world.state = json_obj['state']  # For future things
            return pong_world
    return json_obj


class ClientCommand:
    def __init__(self, from_dict=None):
        self.move_up = False
        self.move_down = False
        self.action = False

        if from_dict is not None and isinstance(from_dict, dict):
            self.update_from_dict(from_dict)
            return

    def clone(self):
        return copy.copy(self)

    def update_from_dict(self, d):
        if not isinstance(d, dict):
            raise TypeError('Argument {} should be a dictionary!'.format(d))
        for k, v in d.items():
            if k in self.__dict__.keys():
                self.__dict__[k] = v

    def json(self):
        return json.dumps(self, default=pong.common.to_json)

    def heading(self):
        dy = 0
        if self.move_up:
            dy = -1
        elif self.move_down:
            dy = +1
        return Vector2(0, dy)
