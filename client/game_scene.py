import asyncio
import pygame as pg
from player import Player


# TODO: once logged in and a ws connection is established, the players data needs to be constantly streamed to the
#  server, and the server needs to stream data from all other players back
class GameScene:

    def __init__(self, screen, connection_manager):
        # set up rendering
        self.screen = screen
        self.players = pg.sprite.Group()
        self.background = pg.surface.Surface(screen.get_size())
        self.background.convert()
        self.background.fill((25, 25, 25))

        # create player character
        self.player = Player(screen.get_size())
        self.players.add(self.player)

        # multiplayer
        self.connection_manager = connection_manager

        # scene management
        self.next_scene = "game_active"

    def add_coplayer(self, coplayer):
        self.players.add(coplayer)

    def update(self):
        self.players.update()
        self.screen.blit(self.background, (0, 0))
        self.players.draw(self.screen)

        #asyncio.run(self.connection_manager.update_positions(data={'position': self.player.position,
               #                                                    'angle': self.player.angle}))

    def handle_key(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.player.accelerate(acceleration=0.1)
            elif event.key == pg.K_DOWN:
                self.player.accelerate(acceleration=-0.1)
            elif event.key == pg.K_LEFT:
                self.player.rotate(speed=-4)
            elif event.key == pg.K_RIGHT:
                self.player.rotate(speed=4)
            elif event.key == pg.K_SPACE:
                asyncio.run(self.connection_manager.test_send(data={'text': 'test'}))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                self.player.accelerate(acceleration=0)
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                self.player.rotate(speed=0)

    def handle_mouse(self, event):
        pass

    def handle_click(self, event):
        pass
