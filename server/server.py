"""Modules used for establishing and handling network connections,
using threads, serializing data, rng, time and pygame"""
import socket
from _thread import start_new_thread
import pickle
from random import randrange
from time import time
import pygame


# initialize networking + socket
SERVER = "172.20.10.2"
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


# initialize anti-cheat constants
MAX_SPEED = 200
MAX_ROT = 200


def anit_cheat_checks(data, player_id):
    """This function is used to run active checks."""
    if not speed_check(data, player_id):
        return False

    if not rotation_check(data, player_id):
        return False

    return True


def speed_check(data, player_id):
    """This function checks if the player has exceeded a preset maximum speed.
    This is done by comparing the currently sent and the last known position,
    while taking the time difference between the two into account."""
    # calculate the distance the player traveled
    current_pos = data[0]
    last_pos = players[player_id][0]

    distance = abs((current_pos - last_pos).length())

    # calculate the time it took
    time_diff = data[3] - players[player_id][3]

    # calculate speed
    speed = distance / time_diff

    if speed > MAX_SPEED:
        print(f"Player {player_id} has exceeded maximum speed ({speed}).")
        return False

    return True


def rotation_check(data, player_id):
    """This function is used to check if the player is exceeding a preset maximum
    rotational speed. This is done by comparing the player's rotation across two received
    packets, while taking the time difference into account."""
    # calculate the change in rotation
    current_rot = data[2]
    last_rot = players[player_id][2]

    angle_change = abs(current_rot - last_rot)

    # calculate the time difference
    time_diff = data[3] - players[player_id][3]

    # calculate speed
    angle_speed = angle_change / time_diff

    if angle_speed > MAX_ROT:
        print(f"Player {player_id} has exceeded maximum rotation speed ({angle_speed}).")
        return False

    return True


def threaded_client(conn):
    """This function starts a new thread which handles a player connection."""
    player_id = generate_key(list(players.keys()))  # store generated key in current thread
    # create data for new player pos, img, rot, current time stamp
    players[player_id] = (pygame.math.Vector2(200, 200), generate_car(), 0, time())
    print(f"{player_id}: {players[player_id]}")  # Debug
    conn.send(pickle.dumps(players[player_id]))  # send new player object to client
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # wait for updated location info from client

            if not data:  # follow up on clean exit by client (initiated via None as sent data)
                print(f"Disconnected\nRemoving player: {player_id}")
                players.pop(player_id)  # remove player from dict
                print(f"Players: {players}")  # Debug
                break

            data = data + (time(),)  # add a time stamp to the data

            if not anit_cheat_checks(data, player_id):
                print(f"Cheating detected\nRemoving player: {player_id}")
                players.pop(player_id)
                print(f"Players: {players}")
                break

            players[player_id] = data  # update dict with new info

            # returns an array containing every player except own
            reply = []
            for k, p in players.items():
                if k != player_id:
                    reply.append(p)

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
