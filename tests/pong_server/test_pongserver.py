import time
import socket
import threading
import unittest

# from tests.constants import *
# import pongserver
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
        self.fake_client = threading.Thread(target=self.fake_client,
                                            args=(self.ps.getsockname(), self.ps.port + 5, self.retd))
        self.fake_client.start()
        self.fake_client.join()
        self.ps.close()

    def test_client_address_retrieved(self):
        ca = self.retd['client_address']
        self.assertNotEqual(ca, self.ps.port)
        print('Got client address:', ca)

    def fake_client(self, server_address, port, return_queue):
        with socket.socket(type=socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.bind(('localhost', port))
            s.sendto('connect'.encode(), server_address)
            # data, _ = s.recvfrom(4096)
            # if data:
            #     if return_queue:
            #         return_queue['player_number'] = int(data.decode('utf-8'))


class PongServerReturnPlayerNumberToClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client_address = ('localhost', 12345)
        self.player_number = 1
        self.retd = dict()  # Dictionary where return values of threads are placed

        self.ps = pongserver.server.PongServer()

        self.client_thread = threading.Thread(target=self.fake_client, args=(self.retd,))
        self.client_thread.start()
        self.server_thread = threading.Thread(target=self.ps.send_player_number, args=(self.client_address, self.player_number))
        self.server_thread.start()

        self.server_thread.join()
        self.client_thread.join()

    def tearDown(self):
        self.ps.close()    # Always remember to close!!!

    def test_player_number_one(self):
        # See if correct player number is handed out.
        self.assertEqual(self.retd['player_number'], self.player_number)
        # The address that the server has sent its player number to gets stored in itself.
        self.assertEqual(self.ps.player_addresses[1], self.client_address)
        # Client handler thread added.
        self.assertEqual(len(self.ps.client_handlers), 1)

    def fake_client(self, return_dict):
        """Client that simulates receiving of player number"""
        with socket.socket(type=socket.SOCK_DGRAM) as s:
            s.bind(self.client_address)
            s.settimeout(2)
            data, address = s.recvfrom(4096)
            if not data:
                return
            decoded = data.decode('utf-8')
            if return_dict is None:
                return
            return_dict['player_number'] = int(decoded)     # Store the result in the return dictionary.


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
        self.client_thread = threading.Thread(target=self.fake_client, args=(self.retd,))

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
        self.assertEqual(self.retd['received_json'], self.ps.pong_world.locations_json())
        print('retd\'s received_json:', self.retd['received_json'])
        print('length:', len(self.retd['received_json']))

    def fake_client(self, retd):
        with socket.socket(type=socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.bind(self.client_address)
            data, address = s.recvfrom(4096)
            if data is None:
                return
            if retd is None:
                raise ValueError('Cannot return value without return dictionary argument!')
            retd['received_json'] = data.decode('utf-8')
