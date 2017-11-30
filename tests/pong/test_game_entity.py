import json
from pygame.math import Vector2
import unittest
import pong.entities as entities


class GameEntityTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_rect_dimensions(self):
        e = entities.GameEntity()
        r = e.get_rect()
        self.assertEqual(r.width, e.WIDTH)
        self.assertEqual(r.height, e.HEIGHT)

    def test_get_location(self):
        e = entities.GameEntity(Vector2(150, 100))
        r = e.get_rect()
        self.assertEqual(r.x, 150)
        self.assertEqual(r.y, 100)

    def test_get_rect_width_height_override(self):
        """Use get_rect with a class that overrides the WIDTH and HEIGHT variables of GameEntity"""
        class TestEntity(entities.GameEntity):
            WIDTH = 20
            HEIGHT = 30
        e = TestEntity()
        r = e.get_rect()
        self.assertEqual(r.width, e.WIDTH)
        self.assertEqual(r.height, e.HEIGHT)


class GameEntityGetCollision(unittest.TestCase):
    def setUp(self):
        self.world = entities.World()
        entities.GameEntity.world = self.world
        self.ent_a = entities.GameEntity((400, 100))
        self.ent_b = entities.GameEntity((400, 100))
        self.ent_c = entities.GameEntity((100, 100))

    def test_get_paddle_collide(self):
        collided = self.ent_a.get_collision()
        self.assertEqual(collided, self.ent_b)

    def test_no_collision(self):
        collided = self.ent_c.get_collision()
        self.assertNotEqual(collided, self.ent_c)
        self.assertIsNone(collided)


class GameEntityNoWorldGetCollision(unittest.TestCase):
    """get_collision method of GameEntity should return None if the entity has no World"""
    def setUp(self):
        entities.GameEntity.world = None
        self.ent = entities.GameEntity()

    def test_no_world(self):
        self.assertIsNone(self.ent.world)

    def test_no_collision(self):
        self.assertIsNone(self.ent.get_collision())


class GameEntityJsonString(unittest.TestCase):
    def setUp(self):
        self.ent = entities.GameEntity()

    def test_jsonify(self):
        j = self.ent.json_string()
        d = json.loads(j)
        print('json:', j)
        print(d)
        self.assertIn('location', d.keys())
        self.assertIn('class_name', d.keys())

        # Compare values
        self.assertEqual((*d['location'],), (*self.ent.location,))
        self.assertEqual(d['class_name'], type(self.ent).__name__)

