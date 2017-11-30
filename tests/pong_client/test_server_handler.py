import unittest
import pong.game as game
from tests.constants import *
import pong_client.client as client


# Don't bother with this yet...
class ServerConnectionThreadInstantiationTestCase(unittest.TestCase):
    def setUp(self):
        self.pong = game.Pong()

    def test_create_connection_thread_with_address_info(self):
        # The address info will be what the connection thread will 'listen' to
        client_handler_address_info = ('localhost', TEST_SERVER_PORT)
        address_info = ('localhost', 10400)
        server_handler = client.ServerHandler(address_info, client_handler_address_info, self.pong)
        self.assertIsNotNone(server_handler.socket)
        self.assertEqual(server_handler.address_info, address_info)
        self.assertEqual(server_handler.client_handler_address_info, client_handler_address_info)


# Don't bother with this yet...
class ServerConnectionThreadTestCase(unittest.TestCase):
    def setUp(self):
        self.client = client.ServerHandler(('localhost', TEST_SERVER_PORT))


    def test_server_reply_with_player_number(self):
        """After connecting to the server, the server's client connection thread sends a message containing the player
        number that this client will be controlling."""
        player_number = self.client.wait_player_number()
        self.assertIn(player_number, (1, 2))    # Either 1 or 2