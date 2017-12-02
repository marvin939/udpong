import pongclient.main
import pongserver.main
import threading


if __name__ == '__main__':
    server = threading.Thread(target=pongserver.main.main)
    server.start()

    for i in range(2):
        t = threading.Thread(target=pongclient.main.main)
        t.start()