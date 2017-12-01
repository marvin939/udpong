import socket


def fake_send_client(string_to_send, bind_address, send_address):
    """Bind a socket to bind_address, and send the string_to_send string to send_address"""
    with socket.socket(type=socket.SOCK_DGRAM) as s:
        s.bind(bind_address)
        s.settimeout(2)
        s.sendto(string_to_send.encode('utf-8'), send_address)


def fake_receive_client(bind_address, return_dict, return_dict_key):
    """Bind a socket to bind_address, and receive bytes from a remote socket,
    then store the decoded bytes into the return_dict using return_dict_key."""
    with socket.socket(type=socket.SOCK_DGRAM) as s:
        s.settimeout(2)
        s.bind(bind_address)
        data, sender_address = s.recvfrom(4096)
        if data is None:
            return
        if return_dict is None:
            raise ValueError('Cannot return value without return dictionary argument!')
        return_dict[return_dict_key] = data.decode('utf-8')
        return_dict['sender_address'] = sender_address
