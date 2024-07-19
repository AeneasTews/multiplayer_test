import socket
import pickle
from player import Player


class Network:
    # wrapper for easy networking using socks
    def __init__(self, server, port):
        # initialize socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        # ipv4 address + port
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            # connect to server
            self.client.connect(self.addr)

            # receive assigned player data from server and generate object
            data = pickle.loads(self.client.recv(2048))
            return Player(data[0], data[1], data[2])

        except socket.error as e:
            print(e)

    def send(self, player):
        try:
            # translate and send current player object to server
            data = (player.position, player.car, player.rotation)
            self.client.send(pickle.dumps(data))

            # receive all other players' data from server and translate
            return [Player(p[0], p[1], p[2]) for p in pickle.loads(self.client.recv(2048))]

        except socket.error as e:
            print(e)

    def disconnect(self):
        try:
            # send no data in order to start clean disconnect process on server
            self.client.send(pickle.dumps(None))
            self.client.close()

        except socket.error as e:
            print(e)
