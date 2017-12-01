import json
import time
import socket
import threading
import unittest

# from tests.constants import *
# import pongserver
import pong.common
import tests.common
import pongserver.server
# import pongserver.server as server
import tests.constants
# from pongserver.server import PongServer, ClientHandler


class PongServerInstantiationTestCase(unittest.TestCase):
    def test_instantiate_no_args(self):
        ps = pongserver.server.PongServer()
        self.assertEqual(ps.port, ps.DEFAULT_PORT)

    def test_instantiate_with_port(self):
        ps = pongserver.server.PongServer(port=tests.constants.TEST_SERVER_PORT)
        self.assertEqual(ps.port, tests.constants.TEST_SERVER_PORT)

    def test_is_a_thread(self):
        ps = pongserver.server.PongServer(port=tests.constants.TEST_SERVER_PORT)
        self.assertTrue(isinstance(ps, (threading.Thread, socket.socket)))


class PongServerTimeoutTestCase(unittest.TestCase):
    def setUp(self):
        self.ps = pongserver.server.PongServer()

    def test_wait_indefinitely_times_out(self):
        """Pong server instance should time out after a few seconds."""
        with self.assertRaises(socket.error):
            data = self.ps.recvfrom(self.ps.BUFFER_SIZE)


class PongServerClientConnectReturnsClientAddress(unittest.TestCase):
    """The server will wait for a connect message from a potential client, and return the client's address."""
    def setUp(self):
        self.ps = pongserver.server.PongServer()
        # self.client_address = self.pongserver.wait_client()
        # self.retq = queue.Queue()
        self.retd = dict()
        self.client_wait_thread = threading.Thread(target=self.ps.wait_client, args=(self.retd,))
        self.client_wait_thread.start()

        self.fake_client = threading.Thread(target=tests.common.fake_send_client,
                                            args=('connect', ('localhost', self.ps.port + 5), self.ps.getsockname(),))
        self.fake_client.start()
        self.fake_client.join()
        self.ps.close()

    def test_client_address_retrieved(self):
        ca = self.retd['client_address']
        self.assertNotEqual(ca, self.ps.port)
        print('Got client address:', ca)


class PongServerReturnPlayerNumberToClientTestCase(unittest.TestCase):
    """Send player number to client."""
    def setUp(self):
        self.client_address = ('localhost', 12345)
        self.player_number = 1
        self.retd = dict()  # Dictionary where return values of threads are placed

        self.ps = pongserver.server.PongServer()

        # self.client_thread = threading.Thread(target=self.fake_client, args=(self.retd,))
        self.client_thread = threading.Thread(target=tests.common.fake_receive_client, args=(self.client_address, self.retd, 'player_number'))
        self.client_thread.start()
        self.server_thread = threading.Thread(target=self.ps.send_player_number, args=(self.client_address, self.player_number))
        self.server_thread.start()

        self.server_thread.join()
        self.client_thread.join()

    def tearDown(self):
        self.ps.close()    # Always remember to close!!!

    def test_player_number_one(self):
        # See if correct player number is handed out.
        self.assertEqual(int(self.retd['player_number']), self.player_number)
        # The address that the server has sent its player number to gets stored in itself.
        self.assertEqual(self.ps.player_addresses[1], self.client_address)
        # Client handler thread added.
        self.assertEqual(len(self.ps.client_handlers), 1)


class PongServerReturnPlayerNumbersToClientsTestCase(unittest.TestCase):
    """Test that the server turns player numbers to both clients."""


class PongServerJoinThreadTestCase(unittest.TestCase):
    """When the join method is called, call the close socket too."""
    def setUp(self):
        self.ps = pongserver.server.PongServer()
        # def fake_run(instance):
        #     pass
        # self.pongserver.run = fake_run
        # This will need to be changed later somehow, so that it doesn't actually call the run function.
        self.ps.start()
        self.ps.join()

    def test_is_dead_after_join(self):
        self.assertFalse(self.ps.is_alive())


class PongServerSocketIsBoundTestCase(unittest.TestCase):
    """When the server gets instantiated, it automatically binds a socket for itself."""
    def setUp(self):
        self.ps = pongserver.server.PongServer()

    def test_test_already_bound(self):
        """Socket raises OSError when it gets bound to the same address more than once"""
        with self.assertRaises(OSError):
            self.ps.bind(('localhost', self.ps.port))

    # class FakeClient:
    #     def __init__(self, port):


class ClientHandlerSendUpdatesTestCase(unittest.TestCase):
    def setUp(self):
        self.ps = pongserver.server.PongServer()
        self.client_address = ('localhost', 11011)
        self.client_handler = pongserver.server.ClientHandler(11020, self.client_address, 1, self.ps)
        self.retd = dict()

        # Thread that sends game update to all clients.
        self.server_thread = threading.Thread(target=self.client_handler.send_game_update)
        # self.client_thread = threading.Thread(target=self.fake_client, args=(self.retd,))
        self.client_thread = threading.Thread(target=tests.common.fake_receive_client, args=(self.client_address, self.retd, 'pong_world_json'))

        # client starts first.
        self.client_thread.start()
        time.sleep(0.1)
        self.server_thread.start()
        self.server_thread.join()
        self.client_thread.join()

    def tearDown(self):
        self.client_handler.close()
        self.ps.close()

    def test_decode_updates(self):
        # self.client
        # self.assertEqual(self.retd['updates'], self.client_handler.jsonify_entities())
        self.assertEqual(self.retd['pong_world_json'], self.ps.pong_world.locations_json())
        print('retd\'s pong_world_json:', self.retd['pong_world_json'])
        print('length:', len(self.retd['pong_world_json']))


class ClientHandlerReceiveClientCommand(unittest.TestCase):
    """When client handler receives a client command from the client, it will update all the entities in
    the pong world (players 1, 2, and ball)"""
    def setUp(self):
        self.retd = dict()
        self.client_address = ('localhost', 10102)
        self.ps = pongserver.server.PongServer()
        self.client_handler = pongserver.server.ClientHandler(10100, self.client_address, 1, self.ps)

        self.cc = pong.common.ClientCommand()
        self.cc.move_up = True
        self.cc.move_down = False
        self.cc.action = True
        self.jcc = json.dumps(self.cc, default=pong.common.to_json, separators=(',', ':'))

        self.client_handler_thread = threading.Thread(target=self.client_handler.receive_client_command, args=(self.retd,))
        self.fake_client_thread = threading.Thread(target=tests.common.fake_send_client, args=(self.jcc,
                                                                                  self.client_address,
                                                                                  self.client_handler.getsockname()))
        self.fake_client_thread.setDaemon(True)

        self.client_handler_thread.start()
        self.fake_client_thread.start()
        self.fake_client_thread.join()
        self.client_handler_thread.join()

    def tearDown(self):
        self.client_handler.close()
        self.ps.close()

    def test_receive_client_command_object(self):
        self.assertIsInstance(self.retd['client_command'], pong.common.ClientCommand)

        cc = self.retd['client_command']
        self.assertEqual(cc.move_up, self.cc.move_up)       # True
        self.assertEqual(cc.move_down, self.cc.move_down)   # False
        self.assertEqual(cc.action, self.cc.action)         # True
