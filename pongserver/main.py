import pongserver.server


def main():
    port = pongserver.server.PongServer.DEFAULT_PORT
    server = pongserver.server.PongServer(port)
    server.start()


if __name__ == '__main__':
    main()
