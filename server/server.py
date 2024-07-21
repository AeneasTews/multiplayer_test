"""Modules used for establishing and handling network connections,
using threads, serializing data, rng and pygame"""
import socket
from _thread import start_new_thread
import pickle
from random import randrange
import pygame

# initialize networking + socket
SERVER = "192.168.178.142"
PORT = 9002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # initialize socket
    s.bind((SERVER, PORT))

except socket.error as e:
    print(e)

# start socket server
s.listen(-1)
print("Server started!\nWaiting for connection...")

# create dict in order to keep track of all players in multiple threads and avoid issues with arrays
players = {}


def generate_car():
    """Abstraction for generating a car image. (Readability)"""
    # generate a random color for the player's square
    return randrange(1, 5)


def generate_key(keys):
    """Used to generate a random key."""
    # generate new key for player dict
    key = randrange(1000000000, 9999999999)
    while key in keys:
        randrange(1000000000, 9999999999)
    return key


def threaded_client(conn):
    """This function starts a new thread which handles a player connection."""
    player_id = generate_key(list(players.keys()))  # store generated key in current thread
    # create data for new player pos, img, rot
    players[player_id] = (pygame.math.Vector2(200, 200), generate_car(), 0)
    print(f"{player_id}: {players[player_id]}")  # Debug
    conn.send(pickle.dumps(players[player_id]))  # send new player object to client
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # wait for updated location info from client
            players[player_id] = data  # update dict with new info

            if not data:  # follow up on clean exit by client (initiated via None as sent data)
                print(f"Disconnected\nRemoving player: {player_id}")
                players.pop(player_id)  # remove player from dict
                print(f"Players: {players}")  # Debug
                break

            # returns an array containing every player except own
            reply = []
            for k, _ in players.items():
                if k != player_id:
                    reply.append(players[k])

            conn.send(pickle.dumps(reply))  # send other players' data to client

        except socket.error as e:
            print(e)
            print(f"Removing player: {player_id}")
            players.pop(player_id)  # remove player from dict
            print(f"Players: {players}")  # Debug
            break

        except EOFError:  # this error is caused by pickle when a client doesn't exit cleanly
            print(f"Lost connection!\nRemoving player: {player_id}")
            players.pop(player_id)  # remove player from dict
            print(f"Players: {players}")  # Debug
            break

    # close connection and exit thread
    conn.close()
    exit()


def main():
    """Main function."""
    while True:
        # accept incoming connections and create socket conn object
        conn, addr = s.accept()
        print(f"Connected: {addr}")

        # start a new thread for every connected client
        start_new_thread(threaded_client, (conn,))


if __name__ == '__main__':
    main()
