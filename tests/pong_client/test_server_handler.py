from pygame.math import Vector2
import pong.game
import tests.common
import unittest
import threading
import pongclient.client
import pongserver.server


SERVER_HANDLER_ADDRESS = ('localhost', 10100)
SERVER_HANDLER_PORT = SERVER_HANDLER_ADDRESS[1]
CLIENT_HANDLER_ADDRESS = ('localhost', 10200)


class ClientConnectToServer(unittest.TestCase):
    """test that the client handler receives server handler's connect request."""
    def setUp(self):
        self.retd = dict()
        self.pong_world = pong.game.Pong()
        self.svh = pongclient.client.ServerHandler(SERVER_HANDLER_ADDRESS, CLIENT_HANDLER_ADDRESS, self.pong_world)
        self.svh_connect_sender_thread = threading.Thread(target=self.svh.connect)

        self.receive_thread = threading.Thread(target=tests.common.fake_receive_client,
                                               args=(CLIENT_HANDLER_ADDRESS, self.retd, 'request'))
        self.receive_thread.start()
        self.svh_connect_sender_thread.start()
        self.svh_connect_sender_thread.join()
        self.receive_thread.join()

    def tearDown(self):
        self.svh.close()

    def test_connect_to_server(self):
        self.assertEqual(self.retd['request'], pongserver.server.PongServer.COMMAND_CLIENT_CONNECT)


class ServerHandlerReceivePlayerNumber(unittest.TestCase):
    def setUp(self):
        self.server_handler_address = ('localhost', 10100)
        self.svh_port = self.server_handler_address[1]
        self.client_handler_address = ('localhost', 10200)
        self.retd = dict()

        self.pong_world = pong.game.Pong()
        self.fake_send_thread = threading.Thread(target=tests.common.fake_send_client,
                                                 args=('1', self.client_handler_address, self.server_handler_address))
        self.svh = pongclient.client.ServerHandler(SERVER_HANDLER_ADDRESS, self.client_handler_address, self.pong_world)

        # Thread that receives the player number
        self.svh_receive_thread = threading.Thread(target=self.svh.receive_player_number, args=(self.retd,))

        self.svh_receive_thread.start()
        self.fake_send_thread.start()
        self.svh_receive_thread.join()
        self.fake_send_thread.join()

    def tearDown(self):
        self.svh.close()

    def test_receive_player_number(self):
        self.assertEqual(self.retd['player_number'], 1)


class ServerHandlerReceiveGameUpdateJSON(unittest.TestCase):
    def setUp(self):
        self.retd = dict()

        self.pong_world = pong.game.Pong()

        # Pong world that resides in the server
        self.server_pong = pong.game.Pong()
        self.server_pong.ball.location = Vector2(33, 33)
        self.locations_json = self.server_pong.locations_json()

        self.fake_send_thread = threading.Thread(target=tests.common.fake_send_client,
                                                 args=(self.locations_json, CLIENT_HANDLER_ADDRESS, SERVER_HANDLER_ADDRESS))
        self.svh = pongclient.client.ServerHandler(SERVER_HANDLER_ADDRESS, CLIENT_HANDLER_ADDRESS, self.pong_world)

        self.svh_update_receiver_thread = threading.Thread(target=self.svh.receive_game_update_json, args=(self.retd,))

        self.svh_update_receiver_thread.start()
        self.fake_send_thread.start()
        self.svh_update_receiver_thread.join()
        self.fake_send_thread.join()

    def tearDown(self):
        self.svh.close()

    def test_receive_player_number(self):
        self.assertEqual(self.retd['game_update_json'], self.locations_json)
        self.pong_world.update_with_json(self.retd['game_update_json'])
        self.assertEqual(self.pong_world.ball.location, self.server_pong.ball.location)
