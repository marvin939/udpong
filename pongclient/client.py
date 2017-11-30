import random
import pongserver.server as server
import threading
import socket
# import pong.game as game
import pong


class Client(socket.socket, threading.Thread):
    BUFFER_SIZE = 4096

    def __init__(self, server_address_info):
        super(socket.socket).__init__(self, type=socket.SOCK_DGRAM)
        super(threading.Thread).__init__(self)
        self.server_address_info = server_address_info
        self.player_number = -1
        self.port_number = self.generate_port_number()

    @staticmethod
    def generate_port_number():
        return random.randint(11000, 20000)

    def run(self):
        pass

    def __del__(self):
        self.close()

    def connect(self):
        with socket.socket(type=socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.sendto(server.PongServer.COMMAND_CLIENT_CONNECT.encode('utf-8'), self.server_address_info)
            data = s.recvfrom(self.BUFFER_SIZE)
            self.player_number = int(data.decode('utf-8'))
            return self.player_number


class ServerHandler(threading.Thread):
    """Thread that handles connections from the server"""
    def __init__(self, address_info, pong):
        self.client_handler_address_info = address_info
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.pong = pong    # The pong world

    def __del__(self):
        self.socket.close()