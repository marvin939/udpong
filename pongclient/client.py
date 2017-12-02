import json
import pongserver.server
import random
import threading
import socket
import pong


class ServerHandler(socket.socket, threading.Thread):
    BUFFER_SIZE = 4096

    def __init__(self, bind_address, server_address, pong_world, client_command=None):
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
        self.settimeout(2)
        self.setDaemon(True)
        self.bind(bind_address)
        self.server_address = server_address
        self.player_number = -1
        # self.port = port
        self.pong_world = pong_world
        self.client_command = client_command

    def run(self):
        self.connect()
        self.player_number = self.receive_player_number()
        while True:
            game_update_json = self.receive_game_update_json()
            self.pong_world.update_with_json(game_update_json)
            self.send_client_command()

    def __del__(self):
        self.close()

    def connect(self):
        self.sendto(pongserver.server.PongServer.COMMAND_CLIENT_CONNECT.encode('utf-8'), self.server_address)
        return

    def receive_player_number(self, return_dict=None):
        data, address = self.recvfrom(self.BUFFER_SIZE)
        if data is None:
            return -1
        decoded = data.decode('utf-8')
        try:
            player_number = int(decoded)
            print('player_number', player_number)
        except ValueError as err:
            raise ValueError(err + ' Should have received an integer!')
        if return_dict is not None and isinstance(return_dict, dict):
            return_dict['player_number'] = player_number

        # OVERWRITE self.server_address to the one received, since that will be address of the client handler
        self.server_address = address

        return player_number

    def receive_game_update_json(self, return_dict=None):
        data, address = self.recvfrom(self.BUFFER_SIZE)
        if data is None:
            raise ValueError('Unable to receive game update!')
            return -1
        decoded_json = data.decode('utf-8')
        try:
            # pong_update = json.loads(decoded_json, object_hook=pong.common.from_json)
            pass
        except json.JSONDecodeError as err:
            raise json.JSONDecodeError(err + ' Not a JSON string!')
        if return_dict is not None and isinstance(return_dict, dict):
            return_dict['game_update_json'] = decoded_json
        return decoded_json

    def send_client_command(self):
        # self.sendto(pongserver.server.PongServer.COMMAND_CLIENT_CONNECT.encode('utf-8'), self.server_address)
        if self.client_command is None:
            print('Unable to send client command: None!')
            return
        self.sendto(self.client_command.json().encode('utf-8'), self.server_address)
        return
