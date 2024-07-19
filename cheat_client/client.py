import pygame
from network import Network

# window initialization
width = 1280
height = 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(window, player, players):
    # draw own player and all sent players on screen
    window.fill((25, 25, 25))
    for p in players:
        p.draw(window)
    player.draw(window)
    pygame.display.update()


def main():
    # initialize networking and get a player object from the server
    network = Network("192.168.178.142", 9002)
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
                exit(0)

            elif event.type == pygame.MOUSEWHEEL:
                player.cheat_rotate(event.y)

        # check input and move own character
        player.move()

        # draw screen
        redraw_window(window, player, players)


if __name__ == '__main__':
    main()
