import time
import threading
import pong.game as game
from tests.constants import *
import pong_server.server as server
import pong_client.client as client
import unittest
import pong.entities as entities


class ClientInstantiationTestCase(unittest.TestCase):

    def test_create_client_with_address_info(self):
        # server_address_info = ('localhost')
        # pong = game.Pong()
        c = client.Client(TEST_SERVER_ADDRESS_INFO)
        self.assertEqual(c.server_address_info, TEST_SERVER_ADDRESS_INFO)

    def test_generate_port_number(self):
        c = client.Client(TEST_SERVER_ADDRESS_INFO)
        self.assertGreater(c.port_number, 10000)


class ClientReplyPlayerNumberTestCase(unittest.TestCase):
    """When the server is setup, it will wait to receive two client messages containing 'connect'.
    The server then replies the player number to the client (depending on the clients' connection order,
    and the client acknowledges this by replying the server handler address info it will use."""
    def setUp(self):
        self.server = server.PongServer()
        self.client_a = client.Client(TEST_SERVER_ADDRESS_INFO)
        self.client_b = client.Client(TEST_SERVER_ADDRESS_INFO)

        self.server_thread = threading.Thread(target=self.server.start)
        self.client_a_thread = threading.Thread(target=self.client_a.connect)
        self.client_a_thread.setDaemon(True)
        self.client_b_thread = threading.Thread(target=self.client_b.connect)
        self.client_b_thread.setDaemon(True)

        self.server_thread.start()
        time.sleep(0.1)
        self.client_a_thread.start()
        self.client_b_thread.start()

    def join(self):
        self.client_a_thread.join()
        self.client_b_thread.join()
        self.server_thread.join()

    def test_send_connect(self):
        self.join()
        # client_a_player_number = self.client_a.connect()    # either gets player 1 or 2
        # client_b_player_number = self.client_b.connect()
        self.assertEqual(self.client_a.player_number + self.client_b.player_number, 3)    # 1 + 2 adds to 3