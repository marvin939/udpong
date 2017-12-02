from pygame.math import Vector2
import pong.common
import unittest


class ClientCommandInstantiation(unittest.TestCase):
    values_dict = {'move_up': True, 'move_down': True, 'action': True, 'attack': False}

    def test_instantiate(self):
        cc = pong.common.ClientCommand()
        self.assertEqual(cc.move_up, False)
        self.assertEqual(cc.move_down, False)
        self.assertEqual(cc.action, False)

    def test_construct_with_dictionary(self):
        cc = pong.common.ClientCommand(self.values_dict)
        self.assertEqual(cc.move_up, self.values_dict['move_up'])
        self.assertEqual(cc.move_down, self.values_dict['move_down'])
        self.assertEqual(cc.action, self.values_dict['action'])


class ClientCommandUpdateFromDictionary(unittest.TestCase):
    def setUp(self):
        self.cc = pong.common.ClientCommand()
        self.values_dict = {'move_up': True, 'move_down': True, 'action': True, 'attack': False}
        # Note: The values_dict contains an unrecognized command 'attack'. This will not be added to the
        # ClientCommand instance

    def test_update_from_dictionary(self):
        self.cc.update_from_dict(self.values_dict)
        self.assertNotIn('attack', self.cc.__dict__.keys())
        self.assertEqual(self.cc.__dict__['move_up'], self.values_dict['move_up'])
        self.assertEqual(self.cc.__dict__['move_down'], self.values_dict['move_down'])
        self.assertEqual(self.cc.__dict__['action'], self.values_dict['action'])


class ClientCommandConstructFromDictionary(unittest.TestCase):
    def setUp(self):
        self.cc = pong.common.ClientCommand()
        self.values_dict = {'move_up': True, 'move_down': True, 'action': True, 'attack': False}

    def test_create_from_dict(self):
        cc2 = pong.common.ClientCommand(self.values_dict)


class ClientCommandGet(unittest.TestCase):
    def setUp(self):
        self.cc = pong.common.ClientCommand()
        self.cc.move_up = True

    def test_get(self):
        cc2 = self.cc.clone()
        self.assertIsInstance(cc2, pong.common.ClientCommand)
        self.assertNotEqual(cc2, self.cc)
        self.assertEqual(cc2.move_up, self.cc.move_up)


class ClientCommandDeriveHeadingMoveDown(unittest.TestCase):
    def setUp(self):
        self.cc = pong.common.ClientCommand()
        self.cc.move_down = True

    def test_get_dir(self):
        heading = self.cc.heading()
        self.assertEqual(heading, Vector2(0, 1))    # Positive Y means going down


class ClientCommandDeriveHeadingMoveUp(unittest.TestCase):
    def setUp(self):
        self.cc = pong.common.ClientCommand()
        self.cc.move_up = True

    def test_get_dir(self):
        heading = self.cc.heading()
        self.assertEqual(heading, Vector2(0, -1))