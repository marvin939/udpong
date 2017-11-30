import queue
import random
import socket
import threading
import time
import unittest

from tests.constants import *


class PongServerInstantiationTestCase(unittest.TestCase):
    def test_instantiate_no_args(self):
        pong_server = server.PongServer()
        self.assertEqual(pong_server.port, pong_server.DEFAULT_PORT)

    def test_instantiate_with_port(self):
        pong_server = server.PongServer(port=TEST_SERVER_PORT)
        self.assertEqual(pong_server.port, TEST_SERVER_PORT)

    def test_is_a_thread(self):
        pong_server = server.PongServer(port=TEST_SERVER_PORT)
        self.assertTrue(isinstance(pong_server, (threading.Thread, socket.socket)))


class PongServerTimeoutTestCase(unittest.TestCase):
    def setUp(self):
        self.pong_server = server.PongServer()

    def test_wait_indefinitely_times_out(self):
        """Pong server instance should time out after a few seconds."""
        with self.assertRaises(socket.error):
            data = self.pong_server.recvfrom(self.pong_server.BUFFER_SIZE)


class PongServerClientConnectReturnsClientAddress(unittest.TestCase):
    """The server will wait for a connect message from a potential client, and return the client's address."""
    def setUp(self):
        self.pong_server = server.PongServer()
        # self.client_address = self.pong_server.wait_client()
        # self.retq = queue.Queue()
        self.retd = dict()
        self.client_wait_thread = threading.Thread(target=self.pong_server.wait_client, args=(self.retd,))
        self.client_wait_thread.start()
        self.fake_client = threading.Thread(target=self.fake_client,
                                            args=(self.pong_server.getsockname(), self.pong_server.port + 5, self.retd))
        self.fake_client.start()
        self.fake_client.join()
        self.pong_server.close()

    def test_client_address_retrieved(self):
        ca = self.retd['client_address']
        self.assertNotEqual(ca, self.pong_server.port)
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

        self.pong_server = server.PongServer()

        self.client_thread = threading.Thread(target=self.fake_client, args=(self.retd,))
        self.client_thread.start()
        self.server_thread = threading.Thread(target=self.pong_server.send_player_number, args=(self.client_address, self.player_number))
        self.server_thread.start()

        self.server_thread.join()
        self.client_thread.join()

    def tearDown(self):
        self.pong_server.close()    # Always remember to close!!!

    def test_player_number_one(self):
        # See if correct player number is handed out.
        self.assertEqual(self.retd['player_number'], self.player_number)
        # The address that the server has sent its player number to gets stored in itself.
        self.assertEqual(self.pong_server.player_addresses[1], self.client_address)
        # Client handler thread added.
        self.assertEqual(len(self.pong_server.client_handlers), 1)

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
        self.pong_server = server.PongServer()
        # def fake_run(instance):
        #     pass
        # self.pong_server.run = fake_run
        # This will need to be changed later somehow, so that it doesn't actually call the run function.
        self.pong_server.start()
        self.pong_server.join()

    def test_is_dead_after_join(self):
        self.assertFalse(self.pong_server.is_alive())


class PongServerSocketIsBoundTestCase(unittest.TestCase):
    """When the server gets instantiated, it automatically binds a socket for itself."""
    def setUp(self):
        self.pong_server = server.PongServer()

    def test_test_already_bound(self):
        """Socket raises OSError when it gets bound to the same address more than once"""
        with self.assertRaises(OSError):
            self.pong_server.bind(('localhost', self.pong_server.port))

    # class FakeClient:
    #     def __init__(self, port):


class PongServerSendUpdatesTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        self.pong_server.close()

    @unittest.skip
    def test_decode_updates(self):
        # self.client
        self.assertEqual(self.retd['updates'], self.pong_server.jsonify_entities())

# class PongServerSocketTestCase(unittest.TestCase):
#     def setUp(self):
#         self.pong_server = server.PongServer()
#
#     def test_socket(self):
#         self.assertIsNotNone(self.pong_server.socket)
#
#
# class PongServerWaitClientConnectionTestCase(unittest.TestCase):
#     def setUp(self):
#         self.pong_server = server.PongServer()
#         self.client_list = []
#         self.server_thread = threading.Thread(target=self.pong_server.wait_clients, args=(self.client_list,))
#         self.c1 = DummyClientThread(self.pong_server.port)
#         self.c2 = DummyClientThread(self.pong_server.port)
#
#     def start_threads(self):
#         self.server_thread.start()
#         time.sleep(0.1)
#         self.c1.start()
#         self.c2.start()
#
#     def join_threads(self):
#         self.server_thread.join()
#         self.c1.join(0.1)
#         self.c2.join(0.1)
#
#     def test_wait_connections(self):
#         """The server will block until its has received two clients that have sent the message 'pong_connect'"""
#         self.start_threads()
#         # self.join_threads()
#         self.server_thread.join()   # Let server thread finish what it's doing.
#         self.assertEqual(len(self.client_list), 2)
#         # Clients are also returned in the client list argument if it's not none.




    # def test_spawn_client_threads(self):
    #     self.start_threads()
    #     client_threads = self.pong_server.create_client_threads(self.client_list)
    #     self.assertEqual(len(self.pong_server.client_threads), 2)
    #     self.assertEqual(len(client_threads), 2)
    #
    #     self.join_threads()



# class DummyServerThread(threading.Thread):
#     def __init__(self, pong_server):
#         super().__init__(name='Pong server thread')
#         self.pong_server = pong_server
#
#     def run(self):
#         self.pong_server.wait_clients()
#         return


# class DummyClientThread(threading.Thread):
#     def __init__(self, name=None, server_port=None):
#         super().__init__()
#         self.name = 'DummyClientThread' if name is None else name
#         self.port = random.randint(10000, 20000)
#         self.socket = socket.socket(type=socket.SOCK_DGRAM)
#         self.server_port = server_port if server_port is not None else server.PongServer.DEFAULT_PORT
#         self.setDaemon(True)
#
#     def run(self):
#         try:
#             self.socket.bind(('localhost', self.port))
#             self.socket.sendto(server.PongServer.COMMAND_CLIENT_CONNECT.encode(), ('localhost', self.server_port))
#         finally:
#             self.socket.close()

# class ServerThreadWaitClientTestCase(unittest.TestCase):
#     def setUp(self):
#         self.server_thread = threading.Thread