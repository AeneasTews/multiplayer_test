"""Modules for exiting,
providing a framework for building games in python,
and simplifying network management"""
import sys
import pygame
from network import Network

# screen initialization
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


def redraw_window(window, player, players):
    """
    Function to draw elements on window and update the display
    :param window: A pygame window / screen
    :param player: A Player object (the own player object)
    :param players: A list of all other player objects
    :return: None
    """
    # draw own player and all sent players on screen
    window.fill((25, 25, 25))
    for p in players:
        p.draw(window)
    player.draw(window)
    pygame.display.update()


def main():
    """Main function"""
    # initialize networking and get a player object from the server
    network = Network("192.168.56.1", 9002)
    player = network.get_player()

    # framerate setup
    clock = pygame.time.Clock()

    while True:
        # 60 fps
        clock.tick(60)

        # send own player's data and receive other players' data
        players = network.send(player)

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
