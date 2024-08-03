"""Modules for exiting,
providing a framework for building games in python,
and simplifying network management"""
import sys
import pygame
from network import Network
from _thread import start_new_thread

# screen initialization
WIDTH = 1280
HEIGHT = 720
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


def check_visible(object_position, player_position):
    """This function checks if an object is visible on screen"""
    return (object_position.x - (WIDTH * 0.55) <= player_position.x <= object_position.x + (WIDTH * 0.55) and
            object_position.y - (HEIGHT * 0.55) <= player_position.y <= object_position.y + (HEIGHT * 0.55))


def redraw_window(window, player, players):
    """
    Function to draw elements on window and update the display
    :param window: A pygame window / screen
    :param player: A Player object (the own player object)
    :param players: A list of all other player objects
    :return: None
    """
    window.fill((25, 25, 25))  # reset background

    # draw every other player with calculated offset
    for p in players:
        if check_visible(p.position, player.position):
            p.draw(window, x=p.position.x + 640 - player.position.x,
                   y=p.position.y + 360 - player.position.y)

    player.draw(window)  # draw player
    pygame.display.update()  # update screen


def main():
    """Main function"""
    # initialize networking and get a player object from the server
    network = Network("192.168.178.142", 9002)
    player = network.get_player()
    players = network.send(player)
    running = True

    def threaded_network():
        nonlocal players
        nonlocal running
        delay = pygame.time.Clock()
        while running:
            # send own player's data and receive other players' data
            players = network.send(player)
            running = False if players is None else True
            delay.tick(FPS / 2)

        network.disconnect()
        sys.exit(0)

    start_new_thread(threaded_network, ())

    # framerate setup
    clock = pygame.time.Clock()

    while True:
        # set FPS
        clock.tick(FPS)

        # check for quit event and close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                network.disconnect()
                pygame.quit()
                sys.exit(0)

        # check input and move own character
        player.move()

        # draw screen
        redraw_window(screen, player, players)


if __name__ == '__main__':
    main()
