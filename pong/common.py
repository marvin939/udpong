import pong.entities as entities
import pong.game as game
import pong.entities
import pong.game
import pygame.math
import json


def convert_to_builtin_type(obj):
    """
    Convert user defined class object into the dictionary for use with JSON.
    This function will be used with json's dump function as the 'default'
    argument.

    Code origin: https://pymotw.com/3/json/     (json_dump_default.py)
    Example:
        json.dumps(obj, default=convert_to_builtin_type)
    """
    d = {
        '__class__': obj.__class__.__name__,
        '__module__': obj.__module__,
    }
    d.update(obj.__dict__)
    return d


def dict_to_object(d):
    """
    Convert a dictionary to an object. This function will be used with json's
    load function as the 'object_hook' argument.
    :param d:
    :return:
    """
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module_ = __import__(module_name)
        class_ = getattr(module_, class_name)
        args = {
            key: value
            for key, value in d.items()
        }
        inst = class_(**args)
    else:
        inst = d
    return inst


def to_json(obj):
    """Converts an object into a JSON-serializable type.
    Original idea: http://www.diveintopython3.net/serializing.html"""
    obj_class = type(obj).__name__

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
                '1': obj.player1,
                '2': obj.player2,
                'b': obj.ball,
                'state': None}
    # future: Add game state; eg. WinnerP1, WinnerP2, Idle (ball hasn't launched), Playing

    raise TypeError(repr(obj) + ' is not JSON serializable!')


def from_json(json_obj):
    """Converts a JSON string into a proper object.
    Original idea: customserializer.py from http://www.diveintopython3.net/serializing.html"""
    if '__class__' in json_obj:
        _class = json_obj['__class__']

        if json_obj['__class__'] == 'Vector2':
            return pygame.math.Vector2(json_obj['__value__'])  # unpack __value__ and turn it into Vector2

        if json_obj['__class__'] == 'Rect':
            return pygame.Rect(json_obj['__value__'])

        if json_obj['__class__'] == 'Ball':
            x, y, w, h = (*json_obj['__value__'],)
            ball = entities.Ball((x, y))
            ball.WIDTH, ball.HEIGHT = w, h
            return ball

        if json_obj['__class__'] == 'Player':
            x, y, w, h = (*json_obj['rect'],)
            player = game.Player(json_obj['number'])
            player.location = pygame.math.Vector2(x, y)
            player.WIDTH, player.HEIGHT = w, h
            player.score = json_obj['score']
            return player

        if _class == 'Pong':
            pong = game.Pong()
            # pong.player =
            pong.player1 = json_obj['1']
            pong.player2 = json_obj['2']
            pong.ball = json_obj['b']
            pong.state = json_obj['state']  # For future things
            return pong

    return json_obj

