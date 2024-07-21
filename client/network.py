"""Modules for establishing and handling network connections,
serializing data and game-specific data."""
import socket
import pickle
from player import Player


class Network:
    """This class acts as a wrapper for easy networking using socks."""
    def __init__(self, server, port):
        # initialize socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        # ipv4 address + port
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        """This function is used for returning the clients own player object
        when a network connection is established for the first time."""
        return self.player

    def connect(self):
        """This function is used to establish the network connection."""
        try:
            # connect to server
            self.client.connect(self.addr)

            # receive assigned player data from server and generate object
            data = pickle.loads(self.client.recv(2048))
            return Player(data[0], data[1], data[2])

        except socket.error as e:
            print(e)
            return None

    def send(self, player):
        """This function is used to send the client's data and receive other players' data."""
        try:
            # translate and send current player object to server
            data = (player.position, player.car, player.rotation)
            self.client.send(pickle.dumps(data))

            # receive all other players' data from server and translate
            return [Player(p[0], p[1], p[2]) for p in pickle.loads(self.client.recv(2048))]

        except socket.error as e:
            print(e)
            return None

    def disconnect(self):
        """This function is used to disconnect the network connection."""
        try:
            # send no data in order to start clean disconnect process on server
            self.client.send(pickle.dumps(None))
            self.client.close()
            return True

        except socket.error as e:
            print(e)
            return False
