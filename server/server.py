import socket
from _thread import *
import pickle
from random import randrange
import pygame

# initialize networking + socket
server = "192.168.178.142"
port = 9002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # initialize socket
    s.bind((server, port))

except socket.error as e:
    print(e)

# start socket server
s.listen(-1)
print("Server started!\nWaiting for connection...")

# create dict in order to keep track of all players in multiple threads and avoid issues with arrays
players = {}


def generate_car():
    # generate a random color for the player's square
    return randrange(1, 5)


def generate_key(keys):
    # generate new key for player dict
    key = randrange(1000000000, 9999999999)
    while keys.__contains__(key):
        randrange(1000000000, 9999999999)
    return key


def threaded_client(conn):
    player_id = generate_key(list(players.keys()))  # store generated key in current thread
    players[player_id] = (pygame.math.Vector2(200, 200), generate_car(), 0)  # create data for new player pos, img, rot
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

            else:
                # returns an array containing every player except own
                reply = []
                for k in players.keys():
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
    while True:
        # accept incoming connections and create socket conn object
        conn, addr = s.accept()
        print(f"Connected: {addr}")

        # start a new thread for every connected client
        start_new_thread(threaded_client, (conn,))


if __name__ == '__main__':
    main()
